### In English:

1. Go to the [Google Cloud Console](https://console.cloud.google.com).  
2. In the navigation menu, click on **IAM & Admin** > **Service Accounts**.  
3. Click **Create Service Account**.  
   - Provide a name for the service account.  
   - Add a description (optional).  
   - Click **Create and Continue**.  
4. Assign the required permissions:  
   - **Storage Object Viewer**: for reading objects in the bucket.  
   - **Storage Object Creator**: for writing objects in the bucket.  
   - **Storage Object Admin**: for full read and write permissions.  
   - After adding the permissions, click **Done**.  
5. In the service account panel, click the three dots on the right of the created account and select **Manage Keys**.  
6. Click **Add Key** > **Create New Key**.  
   - Choose the JSON format.  
   - Download the generated file and save it as `credentials.json` in the root of the project.  

Your environment is now configured to access the Google Cloud bucket.

### Configuration Step: Adding the Bucket Name

Make sure to add the `bucket-name` in the `.env` file. By default,


## Activating the environment  
```bash
make active-environment
```  

## Installing the dependencies
```bash
pip install -r requirements.txt
```  

## Run the project

Finally, to run the project:

```bash
make run
```  


