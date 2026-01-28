from services import get_redis_client
from utils import fetch_pdf_from_s3, extract_text_from_pdf, generate_response, send_email_notification, save_response
from dotenv import load_dotenv


load_dotenv()
r = get_redis_client()

def main():
    print("worker is up!")

    while True:
        file = r.brpop('file_key')
        print(file[1])
        print("**********  START   *********** \n\n")
        print("file received:", file[1])

        pdf_file = fetch_pdf_from_s3(key=file[1])

        print("\n file fetched from s3")

        text = extract_text_from_pdf(pdf_file)

        print("\n text extraction completed")

        response = generate_response(text)

        userEmail = save_response(result = response, resume_name = file[1])

        print("\n response generated")
       
        print("\n sending email")
      
        response = send_email_notification(response, userEmail)
        print(response)
        print("*********  END  *********** \n\n")





if __name__ == "__main__":
    main()


        
