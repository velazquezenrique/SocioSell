# Documentation for Deploying SocioSell on Render

## Overview
This document describes the steps to deploy the **SocioSell** application from the GitHub repository on Render. The application is hosted on port 443, which supports HTTPS. For secure communication, a domain and SSL certificate are required. Additionally, environment variables like `GOOGLE_API_KEY` and `MONGODB_URL` must be configured in the system settings.

## Repository Link
The SocioSell repository can be accessed here:  
**[https://github.com/Varsha-1605/SocioSell](https://github.com/Varsha-1605/SocioSell)**

---

## Prerequisites
1. A Render account.
2. SocioSell GitHub repository access.
3. Required environment variables: `GOOGLE_API_KEY` and `MONGODB_URL`.

---

## Deployment Instructions

### Step 1: Create a New Web Service
1. Log in to your [Render account](https://render.com/).
2. Click on **New +** and select **Web Service**.
3. Connect the **SocioSell** GitHub repository by authorizing Render to access your GitHub account.

### Step 2: Configure Build Settings
1. **Repository Branch**: Select the branch to deploy (e.g., `main`).
2. **Build Command**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Start Command**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 10000
   ```
4. **Environment**: Set Python as the runtime.

### Step 3: Set Environment Variables
1. Go to the **Environment** tab during the setup.
2. Add the following environment variables:
   - **Key**: `GOOGLE_API_KEY`  
     **Value**: `<your-google-api-key>`
   - **Key**: `MONGODB_URL`  
     **Value**: `mongodb+srv://<username>:<password>@cluster.mongodb.net/<database-name>`

### Step 4: Deploy
1. Click **Create Web Service**.
2. Render will build and deploy the application automatically.
3. Monitor the build logs to ensure there are no errors.

### Step 5: Access the Application
1. Once deployed, Render provides a public URL for the application (e.g., `https://sociosell.onrender.com`).
2. To use HTTPS, ensure that your domain and SSL certificate are properly configured in Render settings.

---

## Final Notes
- Ensure `GOOGLE_API_KEY` and `MONGODB_URL` are configured correctly in the environment settings.
- Monitor the application logs on Render for any issues during runtime.
- Use Render’s built-in features for scaling and monitoring to optimize the deployment.
- For secure communication, configure HTTPS with a custom domain and SSL certificate if required.

---

# Documentation for Deploying SocioSell on a Virtual Machine

## Overview
This document describes the steps to deploy the **SocioSell** application from the GitHub repository onto a Virtual Machine (VM) running Windows. The application is hosted on port 443, supporting HTTPS. For secure communication, a domain and SSL certificate are recommended. Additionally, environment variables such as `GOOGLE_API_KEY` and `MONGODB_URL` must be configured in the Windows system settings.

---

## Repository Link
The SocioSell repository can be accessed here:
**[https://github.com/Varsha-1605/SocioSell](https://github.com/Varsha-1605/SocioSell)**

---

## Prerequisites
1. **Virtual Machine**: A Windows-based VM set up on any cloud platform (e.g., Azure, AWS, Google Cloud).
2. **Public IP Address**: Ensure a static public IP is assigned to the VM (e.g., `4.188.74.218`).
3. **Port 443**: Ensure that port 443 is open in both the cloud provider's Network Security Group (NSG) and the Windows Firewall.
4. **Python Version**: Install Python between **3.9 and 3.12**.
5. **Domain and SSL Certificate** (optional): Required for secure HTTPS communication.

---

## Step-by-Step Deployment Instructions

### 1. Install Required Software
#### a. Microsoft C and C++ Build Tools
- Install **Microsoft C++ Build Tools** to ensure compatibility with Python package dependencies.
- Download from: [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

#### b. Python Installation
- Install Python version between **3.9 and 3.12**.
- During installation, ensure the **Add Python to PATH** option is selected.
- Verify installation by running the following command:
  ```bash
  python --version
  ```

### 2. Clone the SocioSell Repository
1. Open **Command Prompt** or **PowerShell** on the VM.
2. Clone the repository using the following command:
   ```bash
   git clone https://github.com/Varsha-1605/SocioSell.git
   ```
3. Navigate to the project directory:
   ```bash
   cd SocioSell
   ```

### 3. Install Python Dependencies
- Install all required Python packages listed in the `requirements.txt` file:
  ```bash
  pip install -r requirements.txt
  ```

### 4. Configure Port 443
#### a. Open Port 443 in Windows Firewall
1. Go to **Control Panel > System and Security > Windows Defender Firewall > Advanced Settings**.
2. Select **Inbound Rules**, and create a new rule to allow traffic on port 443.
3. Allow traffic for required protocols (e.g., TCP).

#### b. Open Port 443 in Cloud Provider NSG
1. Navigate to your cloud platform's portal (e.g., Azure portal).
2. Go to the **Network Security Group** associated with your VM.
3. Add an inbound rule to allow traffic on port 443.

### 5. Configure Environment Variables
To ensure proper functioning of the application, configure the required environment variables:

1. **Open System Settings**:
   - Go to **Control Panel > System > Advanced system settings > Environment Variables**.

2. **Add System Variables**:
   - Click **New** under **System variables** and add the following:
     - **Variable Name**: `GOOGLE_API_KEY`
       **Variable Value**: `<your-google-api-key>`
     - **Variable Name**: `MONGODB_URL`
       **Variable Value**: `mongodb+srv://<username>:<password>@cluster.mongodb.net/<database-name>`

3. **Save and Apply**:
   - Click **OK** to save changes.
   - Restart the system or application to apply changes.

### 6. Access the Application
- The application is hosted on port 443 and can be accessed using the public IP address:
  ```
  https://<private-ip>:443
  ```
- For secure HTTPS access, configure a domain and SSL certificate.

---

## Final Notes
- Ensure that port 443 is open and properly configured in both the Windows Firewall and cloud provider NSG.
- Verify that `GOOGLE_API_KEY` and `MONGODB_URL` environment variables are set correctly.
- For troubleshooting, check logs, network configurations, and ensure all dependencies are installed correctly.
