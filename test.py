import requests
import time

# API endpoint
url = "http://localhost:8000/outfit/process"

# Kullanıcı ID
user_id = "fc39d9f5-dfba-4f5f-bc73-f5638f8e6208"

# Outfit ID ve URL listeleri
outfit_ids = [
    "600a99ed-c28d-4c5a-94d8-d25b274bdb9a",
    "209d62cf-2f57-48b7-8a17-4fc81ceaf4a3",
    "31eddead-1b1f-4af2-ba31-0083781d1368",
    "b837a7b0-bc2a-41cd-8e87-9895513c01e2",
    "83a3d795-1aba-4d39-86a2-ce19b5383b73",
    "12371e52-1391-4ca9-8c58-5c0d096f70bd",
    "af002b4f-1a4a-448c-92e3-e45860715874",
    "4e952c61-bc48-4205-8bf1-d5d13979eca1",
    "0c99a214-8262-465b-9b9b-6c2af75a0291",
    "ee5d618f-128f-4a5a-8983-a21084c49780",
    "7aab76b3-0644-42a4-b172-bf1a6c80d3a8",
    "cd8f6cd9-2767-4473-bb82-411f74b553ca",
    "4aa61973-e4f4-4444-ab07-3b6d8abca7e7",
    "b7bd2540-8a37-429d-b3e1-4a6023e38126",
    "93636e3e-2e17-4762-9aee-7f04bacc6e73",
    "0b65c2e4-5391-49f5-8594-62f898468eee",
    "8edb04f6-7604-47f7-9678-d57b77879370",
    "e066f6ac-4226-433d-9318-b897df804063",
    "67c4f4f4-3d9b-4b9b-89ba-36b3899d2be7",
    "40b41f81-78b5-476c-8a29-56eef585f650",
    "8f6f889c-3188-405d-8574-8fa37d7a8be0",
    "922f21bf-c34e-40e1-9833-786e96b9f9f4",
    "0cc425c4-daf5-4ded-8173-c3ed366c8c3d",
    "5b923363-e058-41dd-b7ca-102d8286a17b",
    "3997df02-4114-456f-b845-a013a8f26d8d",
    "b8eb2094-7bed-413c-9472-d1c6114396e7",
    "8bd883cc-7ed9-4216-84ec-290efc596e0f",
    "fa4d4dc7-460a-4a07-a8cc-5f553b74fb2a",
    "b9cd124c-a4d7-4ab8-9ab9-d914dff41e40",
    "47b330a4-c0ce-43cf-9321-03f37a53775a",
    "e5ddc1f9-4414-4170-8b24-d34d95942e66",
    "c7dba63e-8a93-4f72-abbc-0ebfa6a4d87d",
    "ee44bdd9-93bc-4522-bae5-9a1a15793938",
    "578ebcb2-79e0-4a4f-85a2-210152f81e98",
    "e81ef817-37b5-416f-8f94-63627d41a795",
    "24f1d759-9581-44e6-91a6-184ac1cea3a8",
    "2e693785-7a3b-4dc1-a3ec-026475095af2",
    "14eae9d1-0d24-45b2-be12-a896250d54d9",
    "08c36809-1902-4f5b-ac5b-9589037a4729",
    "6830bd1e-9715-4d6b-9dc2-92f096b27153",
    "f498a298-8011-42aa-a840-1f3db080963b",
    "2043b5f6-fda4-4bd4-8297-8630cbe30771",
    "6952b115-8914-4698-a3f3-c05e6389ba54",
    "e393c401-2f90-4214-b8e7-88fff8ee43d9",
    "7dfa0e6a-eb11-4c55-92b8-ca5727531060",
    "1d9946b3-2eaa-443c-9372-d17b979e187b",
    "78a1e6f2-384d-44e9-9395-775665fbb4ca",
    "91ac401a-05dd-4bb3-b769-597b5792b0e6",
    "f66fedc5-73a0-42d4-a400-8dc9c2d965f6",
    "a457346f-86fe-479a-a94a-779d093f9970",
    "07fc243f-303a-45e2-a1bb-bde964596ce0",
    "3d127bb4-3147-4f9c-8705-029427183154",
    "7fa3d5c6-dada-45a1-8fcf-b9c6ca16854c",
    "9f6ca938-63fc-4c07-8088-31570449551b",
    "c4ab91fa-53e7-4625-b32c-7c11c9bcaae6",
    "c1269997-1cd9-4ba5-8583-f1e42904437b",
    "faf81183-e2e1-47d1-880d-fd7fd9a7dfda",
    "94bef9f7-a8c7-4015-9024-e22a7e5b4aa5",
    "5490c509-7c58-4360-a593-e20bcb4603cf",
    "b8a5add6-51a9-47e7-b156-94dc06cdebd3",
    "2a38f409-e6d6-4fd8-b8c0-bd235caac7ed",
    "e8e49728-3f6d-4313-b7f2-f7eada2b7c24"
  ]

image_urls = [
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/aa28dd5a-80eb-4379-b51e-b3f982bf6c66//146e4b7e-9e9b-4a95-b304-87e8c2ce78c4/outfit.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/aa28dd5a-80eb-4379-b51e-b3f982bf6c66//8f6c3f40-a96d-47f9-b8a4-6f25dd1ac841/outfit.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/aa28dd5a-80eb-4379-b51e-b3f982bf6c66//cacbe43d-e5c1-4bfc-912f-90eaac0348c9/outfit.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/aa28dd5a-80eb-4379-b51e-b3f982bf6c66//23cd8df9-05f4-4c97-8a1a-20b5251ff639/outfit.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/aa28dd5a-80eb-4379-b51e-b3f982bf6c66//c08b9ea6-6bc9-4317-a66b-bc8dea86d543/outfit.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/aa28dd5a-80eb-4379-b51e-b3f982bf6c66//7719dbc9-0e2b-46e5-b122-f045f855e28c/outfit.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/aa28dd5a-80eb-4379-b51e-b3f982bf6c66//a4a5baa8-7ee6-4a1f-844d-d2283ac555c7/outfit.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/aa28dd5a-80eb-4379-b51e-b3f982bf6c66/user-outfits/fd57fa27-7099-473f-a076-f7dc2e74f623/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/aa28dd5a-80eb-4379-b51e-b3f982bf6c66/user-outfits/77b4dd89-d7ab-429f-a902-88c567738c51/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/aa28dd5a-80eb-4379-b51e-b3f982bf6c66/user-outfits/bc7b7e4f-adc0-4a90-81d2-36da9a1c8a46/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/aa28dd5a-80eb-4379-b51e-b3f982bf6c66/user-outfits/ec288d4b-0d8e-42af-9898-5d88d25a4879/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/aa28dd5a-80eb-4379-b51e-b3f982bf6c66/user-outfits/2831826a-a7d2-4ae6-9094-24ab6b8923bd/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/aa28dd5a-80eb-4379-b51e-b3f982bf6c66/user-outfits/e4b82a57-8095-4a15-bebf-0a7594dfc12e/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/aa28dd5a-80eb-4379-b51e-b3f982bf6c66/user-outfits/605a2f4d-147e-4a11-8c53-cd3b46266b6b/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/9380bd41-ddd9-4033-b921-c7ae014305cf/user-outfits/a6c1c058-adec-438b-9d57-c3849ea24f48/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/aa28dd5a-80eb-4379-b51e-b3f982bf6c66/user-outfits/65cb0dbb-da10-49e6-abc1-d321a3a0efd2/outfit-image.png",
"https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/c2ca7581-20db-4c2f-8377-93122df96e7a/user-outfits/4e777174-e38c-4a64-a983-5afa7cede11a/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/79bf841d-21d1-47a9-8647-fa5009a766f4/user-outfits/d3889294-6ba9-46ee-b51c-51d611c0a332/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/79bf841d-21d1-47a9-8647-fa5009a766f4/user-outfits/76d1361b-6622-4b66-91e1-d8b2bfbc3686/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/79bf841d-21d1-47a9-8647-fa5009a766f4/user-outfits/4b5ba0f5-a148-4e3a-8c82-cec1838196ce/outfit-image.png",
 "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/79bf841d-21d1-47a9-8647-fa5009a766f4/user-outfits/8dade860-d56d-419a-905a-9a0c59d754f5/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/79bf841d-21d1-47a9-8647-fa5009a766f4/user-outfits/62ac2f9e-09fe-4732-9e57-f101799ce6e6/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/79bf841d-21d1-47a9-8647-fa5009a766f4/user-outfits/71a35569-692c-47bc-a3d6-626b054ed56f/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/79bf841d-21d1-47a9-8647-fa5009a766f4/user-outfits/6a199a20-c03a-49e6-97f3-b193808dfa24/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/79bf841d-21d1-47a9-8647-fa5009a766f4/user-outfits/09efa985-865f-4c39-9c03-c529bae2f118/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/79bf841d-21d1-47a9-8647-fa5009a766f4/user-outfits/b062e42a-231e-4938-81ab-84eeb63b7d80/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/79bf841d-21d1-47a9-8647-fa5009a766f4/user-outfits/ea88a7e0-ea18-4c90-959f-c9da46be3cc6/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/79bf841d-21d1-47a9-8647-fa5009a766f4/user-outfits/fdfa1675-eef2-4de8-a073-050315eb16fc/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/79bf841d-21d1-47a9-8647-fa5009a766f4/user-outfits/8a5191a1-1b05-4fc5-ad99-7ffb12ad6b89/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/79bf841d-21d1-47a9-8647-fa5009a766f4/user-outfits/4ec74d0d-b13a-4143-9e8b-2100cda9b71a/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/79bf841d-21d1-47a9-8647-fa5009a766f4/user-outfits/b225c8b2-8d0e-41a5-9b31-1d86f1c9f919/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/79bf841d-21d1-47a9-8647-fa5009a766f4/user-outfits/982f89fb-a428-4a97-94ff-3556e62bf169/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/970bd306-5972-4655-8b18-41fda3952019/user-outfits/6cb04030-3161-4423-9f85-db936db12f89/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/970bd306-5972-4655-8b18-41fda3952019/user-outfits/59540506-27bf-473f-801a-ca5c84fd35a8/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/77188b15-15f7-41ac-a05b-3f9a442c76d9/user-outfits/eea44399-9d94-40b9-a93c-408f9046b06f/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/5cadcc45-1843-4715-9d12-af106057e8a7/user-outfits/3817caa7-db53-4518-b61b-425f03c1e01c/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/15ef48db-4849-435c-a0a5-c5a75459ad45/user-outfits/d73292dc-3c13-4c01-92e7-27c04079a751/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/f38d67a0-2fcf-41c0-8189-47d7813a0fa4/user-outfits/ca1e1262-1df7-4930-8dcd-8a955a4331b6/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/f38d67a0-2fcf-41c0-8189-47d7813a0fa4/user-outfits/8c39bc73-5a1c-4562-80ee-ac4599294eec/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/fc39d9f5-dfba-4f5f-bc73-f5638f8e6208/user-outfits/d6c1c223-e0ac-4a41-8d4f-74d653da9cd6/outfit-image.png",

  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/bab43da2-c2b0-47bb-a0a4-fc9891f958d4/user-outfits/a922bb5e-a712-4dde-89fb-4cb92bd5b82c/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/427e593d-0ba3-4372-95ab-acb82101dcb4/user-outfits/23a3c34b-bef3-4fba-9a17-3e701ec3a1e7/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/316cce1d-8074-4600-bc43-6798f08c90ff/user-outfits/c4ef4100-377a-4b35-a9e0-c02606544878/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/316cce1d-8074-4600-bc43-6798f08c90ff/user-outfits/7aa4b5a4-0e35-4b4b-9b2b-d261472a173c/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/ef4a5180-782e-42b2-8ccd-ea2cb88b1084/user-outfits/6b14f6b6-ec79-48f2-a681-f640cdc2b530/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/0c0445a9-44f9-4b70-b013-339bbb794e65/user-outfits/2f8d2a00-12f5-4427-8e84-43025620395d/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/32dad641-7733-4070-bf70-8fb067500a77/user-outfits/e629b40f-4adc-4e67-9c3f-4d3e2a9ec230/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/8f39e9d6-0aad-42bf-8df1-a835c388b6bf/user-outfits/8399e184-8238-4b08-b09a-9abca67a43ce/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/dc254044-747f-49a9-9b63-48b4109ba7d5/user-outfits/76f08bd4-62da-46fe-aaf5-328e612d60ff/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/7f55a217-b3fe-42bf-a07e-02e34efa5132/user-outfits/ba525a9b-0458-482c-98c5-897d803dd19e/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/9380bd41-ddd9-4033-b921-c7ae014305cf/user-outfits/67ab2eef-cf05-48a6-a13d-41d7cf8810b8/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/dc254044-747f-49a9-9b63-48b4109ba7d5/user-outfits/b0bc7386-fa96-42c4-aca5-f30a1472a22e/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/dc254044-747f-49a9-9b63-48b4109ba7d5/user-outfits/7872c5bd-b184-43b7-8e28-2a7772628970/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/7aef66db-4e18-4601-bf6b-f2983263393b/user-outfits/a1d259fd-117c-4d1c-9e7b-b1b808b1fd52/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/dc254044-747f-49a9-9b63-48b4109ba7d5/user-outfits/12ed21c4-ab54-4f2a-8ec3-7e1fdf3bdb9a/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/7aef66db-4e18-4601-bf6b-f2983263393b/user-outfits/eafd8567-d27e-450e-8bf0-3aebced4c7a2/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/7aef66db-4e18-4601-bf6b-f2983263393b/user-outfits/35a0d46a-c3d0-4b1f-b9bb-36f546e1d3f1/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/7aef66db-4e18-4601-bf6b-f2983263393b/user-outfits/5b6de574-49ea-48c7-b410-41b1f3fcb292/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/9380bd41-ddd9-4033-b921-c7ae014305cf/user-outfits/631151e2-136a-4e82-8876-d1ec1b4e8b5d/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/9380bd41-ddd9-4033-b921-c7ae014305cf/user-outfits/c62c5e7b-0fe3-44b8-9d74-75b476aa2932/outfit-image.png",
"https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/9380bd41-ddd9-4033-b921-c7ae014305cf/user-outfits/d162eb87-e574-4d7e-ab30-a88722f5fc7c/outfit-image.png",
  "https://akrxtjnuguvceywyadab.supabase.co/storage/v1/object/public/outfits/fb74cb43-bcb9-4acc-9aff-e55321481636/user-outfits/66fc3ce2-9110-4cfc-bb9a-b61e3cf8dc9f/outfit-image.png"
]

# Form-data tuple format → aynı key tekrar tekrar gönderilir
form_data = [
    ("user_id", user_id),
]

for oid in outfit_ids:
    form_data.append(("outfit_ids", oid))

for url_val in image_urls:
    form_data.append(("outfit_urls", url_val))

# İsteği gönder
response = requests.post(url, data=form_data)

print("Status:", response.status_code)
try:
    print("Response:", response.json())
except Exception:
    print("Raw Response:", response.text)