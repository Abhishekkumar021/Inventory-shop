# Inventory Shop

The Inventory Shop Application is a versatile and streamlined solution designed to manage inventory effectively within a retail setting.
This application primarily focuses on organizing and tracking details related to individual boxes in the inventory.
Leveraging minimal code for maximum efficiency, the application incorporates a range of built-in features and follows best practices for web development.
***
## About
This is Django based project to manage the box operation in an inventory shop
***
# Samples for Testing API
#### 1. Getting Token
*   Use your user name and password  
🚀 Url : [GetAPI](https://boxshop.pythonanywhere.com/api/token) or https://boxshop.pythonanywhere.com/api/token
    
    ![Token Api Image](https://github.com/Abhishekkumar021/Inventory-shop/assets/78357696/1e2cb055-9b40-40d7-a31a-2022511cca35)
*   Click on Post Button and you will get Access token, this token will valid for 24 hours and this will used to access following below APIs
    
---

#### 2. Adding Box
*   Use your Staff-User Token  
🚀 url : [GetAPI](https://boxshop.pythonanywhere.com/add) or https://boxshop.pythonanywhere.com/add
*   These are the samples on Thunder Client  
***Data Format Image***
    ![Data format](https://github.com/Abhishekkumar021/Inventory-shop/assets/78357696/708b3355-0cd3-4fda-96a4-1559cf8a7724)
***Authentication Header Image***
    ![Authentication Token](https://github.com/Abhishekkumar021/Inventory-shop/assets/78357696/53ec0d46-2f47-43b5-9553-5c6378562f9f)
*    Click on Send Button and you will get Status code and Response

---

#### 3. Updating The Box
*   Use your Staff-User Token  
🚀 url : [GetAPI](https://boxshop.pythonanywhere.com/add) or https://boxshop.pythonanywhere.com/add
*   These are the samples on Thunder Client  
***Data Format Image***
    ![Data format](https://github.com/Abhishekkumar021/Inventory-shop/assets/78357696/708b3355-0cd3-4fda-96a4-1559cf8a7724)
[🚀 ***Authentication Token will Sent Same as Adding Box*** 🚀](#2-Adding-Box)
*    Click on Send Button and you will get Status code and Response

---

#### 4. Delete The Box
*   Use your Staff-User Token  
🚀 url : [GetAPI](https://boxshop.pythonanywhere.com/delete/0) or https://boxshop.pythonanywhere.com/delete/box_id  
***Note : Enter box_id (To be deleted) and Requesting user must be owner of the box***
*   These are the samples on Thunder Client  
***Url format and Authentication Token***
    ![Url format and Authentication Token](https://github.com/Abhishekkumar021/Bitwise-Operator/assets/78357696/339f176c-28c9-4c84-9f69-b92303bdba1f)
---
#### 5. List All Boxes
*   Use your Staff-User Token  
🚀 url : [GetAPI](https://boxshop.pythonanywhere.com/list) or https://boxshop.pythonanywhere.com/list  
***Filter Url Samples***  
🚀 <https://boxshop.pythonanywhere.com/list/?length-more-than=1>  
🚀 <https://boxshop.pythonanywhere.com/list/?length-more-than=1&height-more-than=1>  
***Note : Authentication Token can be sent only if all the details of the Boxes, such as Created_by, are required. Otherwise, only a few details will be shown.***
*   These are the samples on Thunder Client  
***Url format and Authentication Token***
    ![Url format and Authentication Token](https://github.com/Abhishekkumar021/Bitwise-Operator/assets/78357696/858236d9-f2ac-44c9-b2b2-ad0d139dabed)
---

#### 6. List All My Boxes
*   Use your Staff-User Token  
🚀 url : [GetAPI](https://boxshop.pythonanywhere.com/list/my) or https://boxshop.pythonanywhere.com/list/my  
***Filter Url Samples***  
🚀 <https://boxshop.pythonanywhere.com/list/my/?length-more-than=1>  
🚀 <https://boxshop.pythonanywhere.com/list/my/?length-more-than=1&height-more-than=1>  
***Note : Authentication Token required***
*   These are the samples on Thunder Client  
***Url format and Authentication Token***
    ![Url format and Authentication Token](https://github.com/Abhishekkumar021/Bitwise-Operator/assets/78357696/db5bc022-621d-41c0-9a4d-a480c5b9d8bd)
---
