/**
 * services/logger.js — Structured Logging & Amazon CloudWatch Logs Integration
 * Streams application and security events to AWS CloudWatch Logs while sanitizing secrets.
 */

const {
  CloudWatchLogsClient,
  CreateLogStreamCommand,
  PutLogEventsCommand,
  DescribeLogStreamsCommand,
} = require('@aws-sdk/client-cloudwatch-logs');

const region = process.env.AWS_REGION || process.env.AWS_DEFAULT_REGION || 'ap-south-1';
const logGroupName = process.env.CLOUDWATCH_LOG_GROUP;
const logStreamName = process.env.CLOUDWATCH_LOG_STREAM || `instance-${process.pid}-${Date.now()}`;

let cwClient = null;
let sequenceToken = null;
let isCwReady = false;

if (logGroupName && process.env.ENABLE_CLOUDWATCH_LOGS === 'true') {
  cwClient = new CloudWatchLogsClient({ region });
  initCloudWatch();
}

async function initCloudWatch() {
  try {
    // Create the log stream if needed
    try {
      await cwClient.send(new CreateLogStreamCommand({
        logGroupName,
        logStreamName,
      }));
    } catch (e) {
      // Ignore if stream already exists
    }

    // Retrieve sequence token if required
    const desc = await cwClient.send(new DescribeLogStreamsCommand({
      logGroupName,
      logStreamNamePrefix: logStreamName,
    }));

    if (desc.logStreams && desc.logStreams[0]) {
      sequenceToken = desc.logStreams[0].uploadSequenceToken;
    }

    isCwReady = true;
    console.log(`✅ CloudWatch Logs initialized [Group: ${logGroupName}, Stream: ${logStreamName}]`);
  } catch (err) {
    console.error(`⚠️ CloudWatch Logs initialization warning: ${err.message}`);
    isCwReady = false;
  }
}

/**
 * Sanitize secrets and credentials from logs
 */
function sanitize(message) {
  if (typeof message === 'object') {
    message = JSON.stringify(message);
  }
  return message
    .replace(/(password|jwt_secret|secret|token|api_key)=['"]?[^'"\s&]+['"]?/gi, '$1=***REDACTED***')
    .replace(/Bearer\s+[A-Za-z0-9-_=.]+/gi, 'Bearer ***REDACTED***');
}

/**
 * Log message locally and asynchronously to CloudWatch
 */
function log(level, message, meta = {}) {
  const timestamp = new Date().toISOString();
  const sanitizedMsg = sanitize(message);
  const formattedConsole = `[${timestamp}] [${level}] ${sanitizedMsg}`;

  if (level === 'ERROR') {
    console.error(formattedConsole, meta);
  } else if (level === 'WARN') {
    console.warn(formattedConsole, meta);
  } else {
    console.log(formattedConsole, meta);
  }

  // Asynchronously send to CloudWatch Logs
  if (isCwReady && cwClient) {
    const logEvent = {
      timestamp: Date.now(),
      message: JSON.stringify({
        timestamp,
        level,
        message: sanitizedMsg,
        meta,
      }),
    };

    cwClient.send(new PutLogEventsCommand({
      logGroupName,
      logStreamName,
      logEvents: [logEvent],
      sequenceToken,
    })).then((res) => {
      sequenceToken = res.nextSequenceToken;
    }).catch((cwErr) => {
      // Don't crash application on logging error
    });
  }
}

module.exports = {
  info: (msg, meta) => log('INFO', msg, meta),
  warn: (msg, meta) => log('WARN', msg, meta),
  error: (msg, meta) => log('ERROR', msg, meta),
};

