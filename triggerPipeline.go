package main

import (
	"bytes"
	"encoding/base64"
	"fmt"
	"net/http"
)

func main() {
	organization := "<YOUR_ORGANIZATION_NAME>"
	project := "<YOUR_PROJECT_NAME>"
	pipelineID := "<YOUR_PIPELINE_ID>"
	accessToken := "<YOUR_PERSONAL_ACCESS_TOKEN>"

	url := fmt.Sprintf("https://dev.azure.com/%s/%s/_apis/pipelines/%s/runs?api-version=6.0-preview.1", organization, project, pipelineID)

	client := &http.Client{}
	req, err := http.NewRequest("POST", url, nil)
	if err != nil {
		fmt.Println("Failed to create request:", err)
		return
	}

	req.SetBasicAuth("", accessToken)

	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Failed to trigger pipeline:", err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusOK {
		fmt.Println("Pipeline triggered successfully")
	} else {
		fmt.Println("Failed to trigger pipeline. Status code:", resp.StatusCode)
	}
}
