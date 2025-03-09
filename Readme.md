
# 🏛️ **LawLens AI - Industrial Compliance Assistant**

## 🚀 Project Description
LawLens AI is an **AI-powered industrial compliance assistant** designed to automate the evaluation of **industrial approval applications** by verifying them against **government regulations**. Using **Retrieval-Augmented Generation (RAG)** in conjunction with **ChromaDB** and **Mistral-7B**, it ensures **environmental, safety, and legal compliance** in industrial projects. 

In the current landscape of **Kerala, India**, industries, small-scale businesses, and individuals seeking to establish factories or renew their licenses often face delays due to manual verification of documents, lengthy processes, and poor communication with government officials. **LawLens AI** aims to address these inefficiencies by providing an intelligent solution that streamlines the approval process and helps both the regulatory bodies and applicants save time, reduce errors, and ensure smoother processing.

This platform is beneficial for **industries, regulatory bodies, and government agencies** by providing faster analysis of industrial applications, detecting potential violations, and generating **detailed compliance reports** on-the-spot.

## 🛠 Tech Stack

- **FastAPI** (Python)
- **ChromaDB** (Vector database for document retrieval)
- **Mistral-7B** (Large Language Model for compliance queries)
- **Sentence-Transformers** (BERT-based sentence embeddings for document understanding)

---

## 🧐 Problem Statement

In the current scenario in **Kerala**, when an individual or company wishes to start the construction of a factory, small-scale business, or even renew a license, they must visit the **Panchayat** or **Municipal Corporation** to get the required permissions. The applicant has to submit a significant amount of paperwork, which the officers later review. However, this process is time-consuming and prone to errors. The officer doesn't always know whether the approval documents contain all necessary supporting documents, if they adhere to **Kerala Government** regulations, or if the necessary steps are being followed according to **Central Government** guidelines.

The two main issues are:
1. Government officers take longer to process and verify documents.
2. Applicants have to wait for long periods and travel multiple times to ensure they have provided all the required documents and permissions from different government departments.

## 💡 Solution

To address these issues, **LawLens AI** provides the following solutions:

1. **RAG-based Agent for Document Analysis and Verification**:  
   This AI agent can communicate with other government agents to verify the required proofs. It reviews the application documents and cross-verifies them with the submitted proofs. The agent generates a summary of what is missing or mismatched and identifies any violations of regulations, which helps the officer provide immediate feedback to the applicant. This reduces the officer's workload and accelerates the approval process.
   
2. **AI Chatbot for Public Access**:  
   This publicly available chatbot provides individuals with easy access to information regarding the documents they need, the required permissions, and the departments they need to contact for verification. The chatbot guides applicants through the process of starting a business or factory, saving them time and effort.

## 🌍 SDG Goals

This project aligns with the following **Sustainable Development Goals (SDGs)**:

- **SDG 11: Sustainable Cities and Communities**  
  Promoting efficient industrial approval processes to create sustainable business ecosystems.

- **SDG 7: Affordable and Clean Energy**  
  Encouraging industries to comply with sustainable energy standards.

- **SDG 13: Climate Action**  
  Helping industries comply with environmental regulations to minimize their carbon footprint.

- **SDG 10: Reduced Inequality**  
  Ensuring equal access to regulatory processes and information for all applicants, regardless of their location or background.

## 🛠 Developer Journey

Initially, our focus was on building a **simple AI chatbot** that could analyze documents and check if the regulations were being followed for industrial license approvals. However, as we delved deeper into the government's approval process, we realized that the real challenge lay in the **document verification** and **proof validation** aspects, which were typically handled manually by the officers. Thus, we evolved our approach to include a **RAG-based agent** that could automate document analysis, cross-check approvals, and communicate with government systems.

By incorporating **Kerala's industrial laws** into our agent’s knowledge base, we were able to create a tool that could significantly reduce the time spent by officers on verifying applications. Finally, to expand our impact, we decided to build a publicly accessible chatbot for those interested in starting businesses or factories, allowing them to easily understand the steps, permissions, and required documentation.

## 🔮 Future Scope

In the future, we plan to:
1. **Expand the AI agent's capabilities** to handle additional verification tasks, including integration with other government systems for real-time updates.
2. **Add language support** to cater to diverse communities in Kerala and other regions.
3. **Implement real-time document tracking** for applicants, where they can see the status of their approval process.
4. **Integrate with mobile apps** to enable access from anywhere, providing even greater convenience for applicants and officers.
5. **Refine the chatbot** to handle more complex queries and offer detailed legal advice related to business and industrial operations.

---

## 🏆 **Acknowledgements**
This project was developed as part of **BeachHack Season 6 - 2025** and won the **First Prize**. 

Team Members:
- **Joel Jaison**
- **Haris Joisn Peter**
- **Namitha P Shaji**

We would like to extend our gratitude to the organizers, mentors, and everyone who supported us during this journey!
