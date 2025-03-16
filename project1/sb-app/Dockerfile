# Use an official OpenJDK runtime as a base image
FROM eclipse-temurin:21-jdk

# Set the working directory inside the container
WORKDIR /app

# Copy the packaged JAR file from the build stage
COPY target/*.jar app.jar

# Expose the application's default port
EXPOSE 8080

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]
