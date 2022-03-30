# adcash-api

## Used python packages
- Flask
- Flask_RESTful
- Flask_SQLAlchemy
- marshmallow
- pytest

## Deploying the application
1. Install required packages
 ```console
pip install -r requirements.txt
```
2. Navigate to the `adcash-api` folder in CMD 

 Run the following command  
 ```console
python app.py
```
3. Or open project in your favourite IDE and run app.py manually

## Endpoints
 `GET /categories` - View all categories  
 `GET /categories/<category_id>` - View a specific category  
 `GET /categories/<category_id>/products` - View all products of a category  
 `POST /categories>` - Add a new category  
 `PUT /categories/<category_id>` - Update category  
 `DELETE /categories/<category_id>` - Delete category  
 
  
 `GET /products` - View all products  
 `GET /products/<product_id>` - View a specific product  
 `POST /products` - Add a new product  
 `PUT /products/<product_id>` - Update product  
 `DELETE /products/<product_id>` - Delete product  
 
 ## Example of creating category and adding a product
 - First create a category, because a product must have a category  
 
 ![post_category](https://user-images.githubusercontent.com/73603187/160734908-4fbf589e-0797-4556-bb3b-28b305690a82.png)  

 - Then create a product and use a category_id of the desired category
 
 ![create product](https://user-images.githubusercontent.com/73603187/160735105-c567843c-1fa0-46ae-bab9-602629aea008.png)
 
 ## Testing
 - If you want to run in CMD then navigate to `adcash-api` folder
 
 Run the command  
  ```console
python -m pytest tests/
```
 - Tests with coverage  
![testing_coverage](https://user-images.githubusercontent.com/73603187/160735592-0b880cb3-2767-4217-abb4-c88610910ce2.png)
