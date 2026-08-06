import { useState } from "react";

import {

  askPolicyQuestion,

} from "./services/api";


function App() {

  const [question, setQuestion] = useState("");

  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState([

    {

      role: "bot",

      text: "Hello! Ask me any question related to your uploaded policy documents."
      
    }

  ]);

  const handleAsk = async () => {

    if (!question.trim()) {

      return;

    }


    const userQuestion = question;


    setMessages((prev) => [

      ...prev,

      {

        role: "user",

        text: userQuestion
      }

    ]);


    setQuestion("");

    setLoading(true);


    try {

      const response =

        await askPolicyQuestion(

          userQuestion

        );


      setMessages((prev) => [

        ...prev,

        {

          role: "bot",

          text: response.answer,

          sources: response.sources || []

        }

      ]);


    } catch (error) {

      console.error(error);


      setMessages((prev) => [

        ...prev,

        {

          role: "bot",

          text: "Failed to get answer from backend."

        }

      ]);


    } finally {

      setLoading(false);

    }

  };


  return (

    <div

      style={{

        backgroundColor: "#f5f7fb",

        minHeight: "100vh",

        display: "flex",

        justifyContent: "center",

        alignItems: "center",

        fontFamily: "Arial"

      }}

    >

      <div

        style={{

          width: "850px",

          height: "760px",

          backgroundColor: "white",

          borderRadius: "12px",

          boxShadow: "0 0 15px rgba(0,0,0,0.1)",

          display: "flex",

          flexDirection: "column",

          overflow: "hidden"

        }}

      >

        <div

          style={{

            padding: "18px 22px",

            backgroundColor: "#2563eb",

            color: "white"

          }}

        >

          <h2

            style={{

              margin: 0

            }}

          >

            Enterprise Policy Chatbot

          </h2>


          <p

            style={{

              margin: "6px 0 0",

              fontSize: "14px"

            }}

          >

          </p>

        </div>


        <div

          style={{

            padding: "15px 20px",

            borderBottom: "1px solid #e5e7eb",

            backgroundColor: "#f9fafb"

          }}

        >

          <p

            style={{

              marginTop: "8px",

              fontSize: "12px",

              color: "#6b7280"

            }}

          >

          </p>

        </div>


        <div

          style={{

            flex: 1,

            padding: "20px",

            overflowY: "auto",

            backgroundColor: "#fafafa"

          }}

        >

          {messages.map((message, index) => (

            <div

              key={index}

              style={{

                display: "flex",

                justifyContent:

                  message.role === "user"

                    ? "flex-end"

                    : "flex-start",

                marginBottom: "15px"

              }}

            >

              <div

                style={{

                  maxWidth: "72%",

                  padding: "12px",

                  borderRadius: "12px",

                  whiteSpace: "pre-wrap",

                  lineHeight: "1.5",

                  textAlign:
                  
                    message.role === "bot"

                      ? "center"
                      
                      : "left",   

                  backgroundColor:

                    message.role === "user"

                      ? "#2563eb"

                      : "#e5e7eb",

                  color:

                    message.role === "user"

                      ? "white"

                      : "black"

                }}

              >
                {message.text}

                {message.role === "bot" &&
 
                 message.sources &&
 
                 message.sources.length > 0 && (
 
                  <div
 
                   style={{
 
                    marginTop: "12px",

                    display: "flex",

                    flexDirection: "column",

                    alignItems: "center",
 
                  }}
 
                 >
 
                  {[...new Set(
 
                    message.sources.map(
 
                     (source) => source.page
 
                    )
 
                   )].map((page) => (
 
                     <button
 
                      key={page}
 
                      onClick={() =>
                       window.open(
 
                        `https://policy-chatbot-groq-render-production.up.railway.app/pdf#page=${page}`,
                        "_blank"
 
                      )
 
                     }
 
                     style={{
 
                      border: "none",
 
                      background: "none",
 
                      color: "#2563eb",
 
                      cursor: "pointer",
 
                      padding: 0,
 
                      fontWeight: "bold",
 
                      display: "block",
 
                      marginTop: "5px"
 
                    }}
                        >
                          📄 View Source Page {page}
                        </button>
                      
                      ))}
                    </div>
                    
                  )}
              </div>

            </div>
          ))}       


          {loading && (

            <div

              style={{

                display: "flex",

                justifyContent: "flex-start"

              }}

            >

              <div

                style={{

                  backgroundColor: "#e5e7eb",

                  padding: "12px",

                  borderRadius: "12px"

                }}

              >
                

                Generating answer...

               </div>

            </div>

          )}

        </div>


        <div

          style={{

            display: "flex",

            padding: "15px",

            borderTop: "1px solid #ddd"

          }}

        >

          <input

            type="text"

            value={question}

            placeholder="Ask a policy question..."

            onChange={(e) =>

              setQuestion(

                e.target.value

              )

            }

            onKeyDown={(e) => {

              if (e.key === "Enter") {

                handleAsk();

              }

            }}

            style={{

              flex: 1,

              padding: "12px",

              borderRadius: "8px",

              border: "1px solid #ccc",

              fontSize: "16px"

            }}

          />


          <button

            onClick={handleAsk}

            disabled={loading}

            style={{

              marginLeft: "10px",

              padding: "12px 20px",

              border: "none",

              borderRadius: "8px",

              backgroundColor: "#2563eb",

              color: "white",

              cursor: "pointer"

            }}

          >

            Send

          </button>

        </div>

      </div>
    </div>
  );
}

export default App;