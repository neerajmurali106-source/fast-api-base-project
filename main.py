from fastapi import Depends,FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import product
from database import session,engine
import database_models
from sqlalchemy.orm import Session 


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"]
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "welcome to my api project"



products=[product(id=1,name="phone",description="Budject phone",price=99,quantity=4),
          product(id=2,name="laptop",description="Gamming laptop",price=999,quantity=10),
          product(id=3,name="smart watch",description="Accurate time",price=55,quantity=14),
          product(id=4,name="Table",description="Created from oak woods can see only in amazone forest",price=38,quantity=554),
          ]


def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()



def init_db():
    db = session()
    count =db.query(database_models.product).count
    if count==0:
        for product in products:
           db.add(database_models.product(**product.model_dump()))
        db.commit()
init_db() 



@app.get("/products")
def get_all_products(db: Session=Depends(get_db)):
    db_products =  db.query(database_models.product).all()
    print(db_products)
    return db_products
 


@app.get("/products/{id}")
def get_product_by_id(id: int,db: Session=Depends(get_db)):
    db_product= db.query(database_models.product).filter(database_models.product.id==id).first()
    if db_product:
        return db_product
    return "product not found"



@app.post("/products")
def add_products(product: product,db: Session=Depends(get_db)):
    db.add(database_models.product(**product.model_dump()))
    db.commit()
    return products
   


@app.put("/products/{id}")
def update_product(id:int,product:product,db: Session=Depends(get_db)):
    db_product= db.query(database_models.product).filter(database_models.product.id==id).first()
    if db_product:
        db_product.name=product.name
        db_product.description=product.description
        db_product.price=product.price
        db_product.quantity=product.quantity
        db.commit()
    else:
        return "no product found"



@app.delete("/products/{id}")
def delete_product(id:int,db: Session=Depends(get_db)):
    db_product= db.query(database_models.product).filter(database_models.product.id==id).first()
    if db_product:
       db.delete(db_product)
       db.commit()
    else:
        return "product not found"

                 