import axios from "axios";


const API_URL = "https://policy-chatbot-groq-render-production.up.railway.app";


export const getBackendMessage = async () => {

  const response = await axios.get(API_URL);

  return response.data;

};


export const askPolicyQuestion = async (question) => {

  const response = await axios.post(

    `${API_URL}/api/chat`,

    {

      question: question

    }

  );


  return response.data;

};


export const uploadPdf = async (file) => {

  const formData = new FormData();


  formData.append(

    "file",

    file

  );


  const response = await axios.post(

    `${API_URL}/api/upload`,

    formData,

    {

      headers: {

        "Content-Type": "multipart/form-data"

      }

    }

  );


  return response.data;

};