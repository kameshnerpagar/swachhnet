/**
 * services/sqsService.js — Amazon SQS Asynchronous Job Queue Integration
 * Handles asynchronous notification dispatch, SLA breach escalations, and background audit processing.
 */

const { SQSClient, SendMessageCommand, ReceiveMessageCommand, DeleteMessageCommand } = require('@aws-sdk/client-sqs');

const region = process.env.AWS_REGION || process.env.AWS_DEFAULT_REGION || 'ap-south-1';
const sqsClient = new SQSClient({ region });
const queueUrl = process.env.SQS_QUEUE_URL;

/**
 * Enqueue an asynchronous job to Amazon SQS
 * @param {string} jobType - e.g., 'COMPLAINT_CREATED', 'TRUCK_ASSIGNED', 'SLA_BREACH'
 * @param {object} payload - Job payload
 */
async function enqueueJob(jobType, payload) {
  if (!queueUrl || process.env.USE_MOCK_SQS === 'true') {
    if (process.env.NODE_ENV !== 'production') {
      console.log(`[SQS Mock Queue] Job enqueued: ${jobType}`, JSON.stringify(payload).substring(0, 100));
    }
    return { MessageId: `mock-${Date.now()}` };
  }

  try {
    const messageBody = JSON.stringify({
      jobType,
      payload,
      timestamp: new Date().toISOString(),
    });

    const command = new SendMessageCommand({
      QueueUrl: queueUrl,
      MessageBody: messageBody,
      MessageAttributes: {
        JobType: {
          DataType: 'String',
          StringValue: jobType,
        },
      },
    });

    const response = await sqsClient.send(command);
    return response;
  } catch (err) {
    console.error(`⚠️ SQS enqueue error for [${jobType}]:`, err.message);
    // Don't fail customer-facing request if async queuing hits a temporary glitch
    return null;
  }
}

/**
 * Starts a background consumer worker polling SQS messages
 * @param {Function} messageHandler - Async handler for processed jobs
 */
function startSqsWorker(messageHandler) {
  if (!queueUrl || process.env.USE_MOCK_SQS === 'true') {
    console.log('ℹ️ SQS Worker: Queue URL not configured or in mock mode. Real background polling inactive.');
    return;
  }

  console.log(`🚀 Starting SQS background worker on queue: ${queueUrl}`);
  let isRunning = true;

  const poll = async () => {
    while (isRunning) {
      try {
        const command = new ReceiveMessageCommand({
          QueueUrl: queueUrl,
          MaxNumberOfMessages: 5,
          WaitTimeSeconds: 15, // Long polling to minimize AWS SQS API costs
          VisibilityTimeout: 30,
        });

        const response = await sqsClient.send(command);
        if (response.Messages && response.Messages.length > 0) {
          for (const msg of response.Messages) {
            try {
              const body = JSON.parse(msg.Body);
              await messageHandler(body);

              // Delete processed message
              await sqsClient.send(new DeleteMessageCommand({
                QueueUrl: queueUrl,
                ReceiptHandle: msg.ReceiptHandle,
              }));
            } catch (procErr) {
              console.error('❌ Failed processing SQS message:', procErr.message);
              // Leave message to return to queue or dead-letter queue after visibility timeout
            }
          }
        }
      } catch (err) {
        console.error('⚠️ SQS worker poll error:', err.message);
        await new Promise((res) => setTimeout(res, 5000));
      }
    }
  };

  poll();

  return {
    stop: () => {
      isRunning = false;
    },
  };
}

module.exports = {
  sqsClient,
  enqueueJob,
  startSqsWorker,
};

