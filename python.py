
import requests
import pandas as pd;
def check_status_code(link):
    try:
        response = requests.get(link,verify=False)
        return response.status_code
    except requests.RequestException as e:
        return f"Error: {e}"

new_domain = "https://nativepush.traya.health"
df = pd.read_excel('/home/mukesh/Downloads/MasterLinks.xlsx')
processed= df.iloc[:,[1]].to_numpy()
totalValidLinks=0
totolInvalidValidRequests=0
totalValidReq=0
invalidUrl=[]
for i in range(len(processed)):
    if pd.notna(processed[i][0] ):
        processed[i][0].replace("https://traya.health",new_domain)
        print( processed[i][0])
        totalValidLinks=+1
        res_code=check_status_code(processed[i][0])
        print(res_code)
        if(int(res_code)>305):
            totolInvalidValidRequests+=1
            invalidUrl.append(processed[i][0])
        else:
            totalValidReq+=1
            

print(f"{totolInvalidValidRequests},{totalValidReq},{invalidUrl}")
