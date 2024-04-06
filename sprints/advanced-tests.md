# **Gocod Project Testing Guide**

## **Launching Services with Docker Compose**

Before testing the API endpoints and the front-end application, ensure that the services are up and running using Docker Compose.

### **Steps to Launch Services**
> Before doing this, add the section `env_file: .env` to the section `api` of the `docker-compose.yml` file.
1. Open your terminal.
2. Navigate to the root directory of your project where the **`docker-compose.yml`** file is located.
3. Run the command: **`docker-compose up`**. This will start the services defined in your Docker Compose file, namely the API and the front-end services.

## **Testing API Endpoints with Swagger**

### **Accessing Swagger UI**

1. Ensure the API service is running via Docker.
2. Open a browser and navigate to **`http://localhost:8080/docs`**. This will open the Swagger UI for your API.

### **Testing Endpoints**

- In the Swagger UI, you will see a list of all available endpoints with their respective HTTP methods (GET, POST, etc.).
- To test a specific endpoint, click on it to expand it, then click the **`Try it out`** button.
- Fill in any required parameters and click **`Execute`**.
- You will see the request sent and the response received from the server, including response body and status codes.

## **Testing the Front-End of the Application**

### **Launching the Front-End Application**

1. Ensure the front-end service is running via Docker.
2. Open a browser and navigate to **`http://localhost:3000`**.

### **Functional Testing**

### User Registration and Login

1. **Registration:** Go to the registration page and create a new user account.
2. **Login:** Use the credentials of the newly created account to log into the application.

### Adding Projects and Templates

1. **Add Project:** Navigate to the project management section and try adding a new project, update, view or delete.

2. **Add Template:** Go to the template section and attempt to create a new template.

### **Verifications**

- **Check that data is correctly displayed** in the user interface after each action.
- **Monitor API responses** for each interaction with the front-end to ensure requests are processed correctly.