
```markdown
# Documentation for Deploying SocioSell on Azure Virtual Machine  

## Overview  
This document describes the steps to deploy the **SocioSell** application from the GitHub repository on an Azure Virtual Machine (VM) running Windows. The application is hosted on port 443, which supports HTTPS. However, for secure communication, a domain and SSL certificate are required. Additionally, environment variables like `GOOGLE_API_KEY` and `MONGODB_URL` must be configured in the Windows system settings.

---

## Repository Link  
The SocioSell repository can be accessed here:  
**[https://github.com/Varsha-1605/SocioSell](https://github.com/Varsha-1605/SocioSell)**  

---

## Prerequisites  
1. **Azure Virtual Machine**: A Windows-based VM is set up on Azure.  
2. **Public IP Address**: `4.188.74.218` is assigned to the VM.  
3. **Port 443**: Ensure that port 443 is opened in the Azure Network Security Group (NSG).  
4. **Python Version**: Install Python between **3.9 and 3.12**.  
5. **Domain and SSL Certificate** (optional): Needed for secure HTTPS communication.

---

## Step-by-Step Deployment Instructions  

### 1. Install Required Software  
#### a. Microsoft C and C++ Build Tools  
- Install the **Microsoft C++ Build Tools** to ensure compatibility with Python package dependencies.  
- Download from: [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

#### b. Python Installation  
- Install Python version between **3.9 and 3.12**.  
- Add Python to the system PATH during installation.  
- Verify installation:  
  ```bash
  python --version
  ```

---

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

---

### 3. Install Python Dependencies  
- Install all required Python packages listed in the `requirements.txt` file:  
  ```bash
  pip install -r requirements.txt
  ```

---

### 4. Configure Port 443  
1. Open port 443 in the Windows Firewall:  
   - Go to **Control Panel > System and Security > Windows Defender Firewall > Advanced Settings**.  
   - Select **Inbound Rules**, and create a new rule to open port 443.  
   - Allow traffic for the required protocols.  

2. Ensure port 443 is also allowed in the **Azure Network Security Group (NSG)**:  
   - Navigate to your Azure portal.  
   - Go to your VM's NSG settings and add an inbound rule for port 443.  

---

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
   - Click **OK** to save.  
   - Restart the system or application to ensure the changes take effect.  

---

### 6. Accessing the Application  
- The application is hosted on port 443 and can be accessed using the public IP address:  
  ```  
  http://4.188.74.218:443  
  ```
- Note: To use HTTPS securely, configure a domain and SSL certificate.

---

## Final Notes  
- The site is accessible via the provided public IP but will work securely with a domain and SSL certificate.  
- Ensure that `GOOGLE_API_KEY` and `MONGODB_URL` are configured correctly in the environment variables.  
- For troubleshooting, check logs and network configurations on both the VM and Azure portal.  
```  
