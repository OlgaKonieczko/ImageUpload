1.	Project setup
Build docker image:
docker-compose build
Run container:
docker-compose up


As part of the project, a database was prepared, consisting of 5 models.
-	Size (size, description, created, id)
Contains possible image sizes. Predefined sizes: 400px, 200px, and 0 (in this case, size 0 indicates the original image size). Admin is allowed to create any tier.
-	Tier (tier, description, created, id, sizes, generate_expiring_link)
Contains possible tiers. Each tier can be assigned with available sizes and Boolean defining if generating expiring links is available for this tier. Predefined tiers: ‘Basic’, ‘Premium; ‘Enterprise.’ Admin is allowed to create any tier.
-	Image (image, owner, tier, description, title, created, id) 
Contains images uploaded to db. Each image is assigned to the owner (the user who uploaded it) and inherits the tier from his owner. A signal to update an image tier in case of owner tier change was also introduced. Predefined images are downloaded from www.pexels.com.
-	Profile (user, username, name, email, tier, id)
Contains user profiles. Every profile is assigned a user and tier. When a new user is created, his profile is automatically created with the ‘Basic’ tier, which the user can amend.
Created users:
Username	Password
admin1 	1234
test_basic	IQzT8BUt^er1eCUO
test_premium	@vL60p&!Y%C3ycH*
test_enterprise	k8MtP1MD$lnf^wP$

-	ExpiringLink (resource, token, expiration_timestamp)
Contain tokens necessary to create and validate expiring links.

3. Created urls
-	Homepage - is set up for the login page. If a user is logged in, it will be redirected to his images list.
http://127.0.0.1:8000/ 
-	Logout user
http://127.0.0.1:8000/logout/  
-	Images list - listing user images with all available links for this user tier http://127.0.0.1:8000/images/ 
-	Image – link to image with proper size
http://127.0.0.1:8000/images/image_id/image_size 
e.g., http://127.0.0.1:8000/images/252f46c0-1d3c-42c7-ac3a-b4eb57894223/400  
-	Image upload
http://127.0.0.1:8000/upload/ 
-	Image update - path to update an existing image
http://127.0.0.1:8000/update/image_id 
e.g.: http://127.0.0.1:8000/update/252f46c0-1d3c-42c7-ac3a-b4eb57894223 
-	Image delete - path to delete the existing image
http://127.0.0.1:8000/delete/image_id 
e.g.:http://127.0.0.1:8000/delete/252f46c0-1d3c-42c7-ac3a-b4eb57894223 
-	Generate expiring link
http://127.0.0.1:8000/generate_exp_link/image_id/image_size  
e.g.: http://127.0.0.1:8000/generate_exp_link/252f46c0-1d3c-42c7-ac3a-b4eb57894223/400 
-	Expiring link
http://127.0.0.1:8000/exp_link/image_id/image_size?token=token e.g.:
http://127.0.0.1:8000/exp_link/252f46c0-1d3c-42c7-ac3a-b4eb57894223/400?token=c04b3d3790bcc06bef71ab9c9634850a 

