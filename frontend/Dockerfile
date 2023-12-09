# getting nginx base image using alpine for linux 
FROM nginx:alpine

# adding a custom nginx conf file in to the container replacing the default
COPY default.conf /etc/nginx/conf.d/default.conf

# opening up port 80 for all access to frontend
EXPOSE 80

#defining command to start nginx server. daemon off and -g allows it to run in the backgound.
CMD ["nginx", "-g", "daemon off;"]


