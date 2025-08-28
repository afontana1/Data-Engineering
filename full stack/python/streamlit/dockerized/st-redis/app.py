import streamlit as st
import redis

r = redis.Redis(host='redisdb', port=6379, db=0)

def app():
    st.title('Welcome')
    name = st.text_input('Name and Surname:')
    age = st.number_input('Age:')
    if st.button('Submit'):
        r.set('name', name)
        r.set('age', age)
        st.success('Data is stored successfully!')

if __name__ == "__main__":
    app()