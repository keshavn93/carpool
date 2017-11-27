FROM python:3-onbuild

# specify the port number the container should expose
EXPOSE 9090

# run the application
CMD ["python", "./app.py"]