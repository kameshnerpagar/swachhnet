/**
 * services/ssmService.js — AWS Systems Manager (SSM) Parameter Store Integration
 * Retrieves encrypted application secrets and configurations securely on startup.
 */

const { SSMClient, GetParametersByPathCommand } = require('@aws-sdk/client-ssm');

const region = process.env.AWS_REGION || process.env.AWS_DEFAULT_REGION || 'ap-south-1';
const ssmClient = new SSMClient({ region });

/**
 * Loads parameters from SSM Parameter Store under a designated path prefix
 * (e.g. /swachhnet/prod/) into process.env without exposing plaintext secrets.
 * @param {string} pathPrefix - Parameter path prefix (defaults to /swachhnet/prod/)
 */
async function loadParametersFromSSM(pathPrefix = '/swachhnet/prod/') {
  if (process.env.USE_SSM !== 'true') {
    return;
  }

  try {
    console.log(`🔐 Fetching application configuration from SSM Parameter Store: ${pathPrefix}...`);
    const command = new GetParametersByPathCommand({
      Path: pathPrefix,
      Recursive: true,
      WithDecryption: true,
    });

    const response = await ssmClient.send(command);
    if (!response.Parameters || response.Parameters.length === 0) {
      console.log(`ℹ️ No SSM parameters found at path ${pathPrefix}. Relying on local environment.`);
      return;
    }

    let loadedCount = 0;
    for (const param of response.Parameters) {
      // Extract parameter name: e.g. /swachhnet/prod/DATABASE_URL -> DATABASE_URL
      const key = param.Name.replace(pathPrefix, '');
      if (key && param.Value) {
        process.env[key] = param.Value;
        loadedCount++;
      }
    }

    console.log(`✅ Loaded ${loadedCount} secure parameters from AWS SSM Parameter Store.`);
  } catch (err) {
    console.error(`⚠️ SSM Parameter fetch failed: ${err.message}. Falling back to local environment variables.`);
  }
}

module.exports = {
  loadParametersFromSSM,
};

