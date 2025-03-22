#python image
FROM python:3.9-slim

#working directory
WORKDIR /app
#copy files
COPY . .
#install dependencies
RUN pip install --no-cache-dir -r requirements.txt

#expose port
EXPOSE 5000
#run application
CMD ["gunicon","-b", "0.0.0.0:5000", "app:app"]