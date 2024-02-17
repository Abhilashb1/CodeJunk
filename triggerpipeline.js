const axios = require('axios');

async function triggerPipeline() {
    const organization = '<YOUR_ORGANIZATION_NAME>';
    const project = '<YOUR_PROJECT_NAME>';
    const pipelineId = '<YOUR_PIPELINE_ID>';
    const accessToken = '<YOUR_PERSONAL_ACCESS_TOKEN>';

    const url = `https://dev.azure.com/${organization}/${project}/_apis/pipelines/${pipelineId}/runs?api-version=6.0-preview.1`;

    try {
        const response = await axios.post(url, {}, {
            headers: {
                'Authorization': `Basic ${Buffer.from(`:${accessToken}`).toString('base64')}`
            }
        });
        
        console.log('Pipeline triggered successfully:', response.data);
    } catch (error) {
        console.error('Failed to trigger pipeline:', error.message);
    }
}

triggerPipeline();
