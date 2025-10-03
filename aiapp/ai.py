from openai import OpenAI
from decouple import config

client=OpenAI(api_key=config("OPENAI_API_KEY"))


def get_ai(user_input,conversation):
    
    all_messages=conversation.messages.all().order_by("created_at")


    messages=[
        {"role":"system","content":"you are a helpful assistant"}
        ]
    
    for msg in all_messages:

        if msg.sender=="user":
              role="user"
        else:
               role="assistant" 

        messages.append({
            "role":role, "content":msg.content
        })

    messages.append({"role":"user","content":user_input})

    response=client.chat.completions.create(
         model="gpt-3.5-turbo",
         messages=messages,
         temperature=0.3
    )

    content=response.choices[0].message.content
    return content



