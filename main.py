# import library
from fastapi import FastAPI, HTTPException, Header
import pandas as pd

# create object atau instance untuk FastAPI
app = FastAPI()

# create API KEY
API_Key = "hck024data"

# untuk run, pakai terminal dengan command uvicorn 21_latihan_api:app --reload

# create endpoint home
@app.get("/")
def home():
    return {"message": "Selamat datang di Tokopedia!"}

# create endpoint data
@app.get("/data")
def read_data():
    # untuk read data dari 22_data.csv
    df = pd.read_csv("22_data.csv")
    # mengembalikan data dengan orient="records" agar value ditampilkan per baris
    return df.to_dict(orient="records")

# create endpoint data with number of parameter "id"
@app.get("/data/{number_id}")
def read_item(number_id: int):
    # untuk read data dari 22_data.csv
    df = pd.read_csv("22_data.csv")
       
    # filter data by id
    filter_data = df[df["id"] == number_id]

    # jika data number_id yang diinput tidak ada yang cocok
    if len(filter_data) ==0:
        raise HTTPException(status_code=404, detail="ID barang yang dimasukkan tidak ditemukan")

    # mengembalikan data dengan orient="records" agar value ditampilkan per baris
    return filter_data.to_dict(orient="records")

# create endpoint update file csv 22_data
@app.put("/items/{number_id}")
def update_item(number_id: int, nama_barang: str, harga: float):
    
    # untuk read data dari 22_data.csv
    df = pd.read_csv("22_data.csv")
    
    # create dataframe dari updated input
    updated_df = pd.DataFrame([{
        "id": number_id,
        "nama_barang": nama_barang,
        "harga": harga
    }])
    
    # merge updated df ke dalam original df
    df = pd.concat([df, updated_df], ignore_index=True)
    # save updated df to file csv
    df.to_csv("22_data.csv", index=False)

    return {"message": f"Item dengan ID {number_id} berhasil diperbarui."}

@app.get("/secret")
def read_secret(api_key: str = Header(None)):

    # untuk read data dari 22_data.csv
    secret_df = pd.read_csv("23_secret_data.csv")


    # cek apakah API Key yang diinput sesuai ketentuan
    if api_key != API_Key:
        raise HTTPException(status_code=401, detail="API Key tidak valid")
    return secret_df.to_dict(orient='records')