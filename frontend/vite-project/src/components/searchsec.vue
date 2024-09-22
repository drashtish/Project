<template>
    <div>
      <nav class="navbar">
      <div class="nav-container">
        <div v-if="this.role == 'admin'">
        <RouterLink to="/AD" class="nav-link">Home</RouterLink></div>
        <div v-if="this.role != 'admin'">
        <RouterLink to="/UD" class="nav-link">Home</RouterLink></div>

        <a @click="alogout" class="nav-link">Logout</a>

      </div>
    </nav>
    <form>
      <h2>  Search: </h2><input type="text" v-model="this.find" @input='entry'>
    </form>
    <div>
      


      <div v-if="this.role == 'admin'">
  <h2 v-if="this.sections.length != 0"> Matching Sections </h2>
  <div class="card" v-for="s in sections" :key="s.ID">
    <div>
      <h3><router-link :to="`/adminsbooks/${s.ID}`">{{ s.Title }}</router-link></h3>
    </div>
    <div class="button-box">
      <button @click="dlt(s.ID)">Delete</button>
    </div>
  </div>
  <h2 v-if="this.sections.length == 0">No Matching Sections Found</h2>

  <h2 v-if="this.books.length != 0"> Matching books </h2>
  <div class="card" v-for="a in books" :key="a.ID">
    <div>
      <h3>Title: {{ a.Title }}</h3>
      <p>Author: {{ a.Author }}</p>
      <a :href="`http://localhost:5000/book/${a.ID}.pdf`" target="_blank">Open Book</a><br>
      <RouterLink :to="`/usersnreqs/${a.ID}`">All Users and Requests</RouterLink>
    </div>
    <div class="button-box">
      <button @click="dltbook(a.ID)">Delete</button>
    </div>
  </div>
  <h2 v-if="this.books.length == 0">No Matching Books Found</h2>

</div>



<div v-if="this.role == 'user'">
  <h2 v-if="this.sections.length != 0">Matching Sections</h2>
  <div class="card" v-for="s in sections" :key="s.ID">
    <div>
      <h3><router-link :to="`/usersbooks/${s.ID}`">{{ s.Title }}</router-link></h3>
    </div>
  </div>
    <h2 v-if="this.sections.length == 0">No Matching Sections Found</h2>




<h2 v-if="this.books.length != 0">Matching Books</h2>
  <div class="card" v-for="a in books" :key="a.ID">
    <div>
      <h3>Title: {{ a.Title }}</h3>
      <p>Author: {{ a.Author }}</p>
      <p v-if="a.Status == 'Pending'">Your request is not yet approved, please wait!</p>


<p v-else-if="a.Status == 'Approved'">
        Date of Issue: {{ a.Issuedate }}<br><br>
      </p>

      <p v-else-if="a.Status == 'Rejected'">Sorry to say that! Your request is rejected.</p>

      <p v-else>
        Request this book to read
        <button @click="reqest(a.ID)">Request</button>
      </p>
    </div>
    <div class="button-box" v-if="a.Status == 'Approved'">
      <a :href="`http://localhost:5000/book/${a.ID}.pdf`" target="_blank">Open Book</a>

      <button @click="retrn(a.ID)">Return Back</button>
    </div>
  </div>
    <h2 v-if="this.books.length == 0">No Matching Books Found</h2>

</div>


     
    </div>
    </div>


</template>


  
      




  







<script>
export default {
    name: 'searchsec',
    data() {
        return {
            sections: [],
            books: [],
            find: '',
            token: '',
            role: ''
        };
    },
    methods: {

      alogout(){
        localStorage.clear()
        alert('You have been logged out successfully')
        if(this.role == 'admin'){
          this.$router.push('/adminlogin')
        }
        else{this.$router.push('/')}
  },

    async dltbook(id) {
      try {
        const output = await fetch(`http://localhost:5000/dltbook/${id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authorization': `${this.token}`
          }
        });

        if (!output.ok) {
          const errordata = await output.json();
          throw new Error(errordata.msg || 'An error occurred');
        }

        const data = await output.json();
        alert(data.msg);
        this.entry();
      } catch (error) {
        alert(error.message);
      }
    },

     async dlt(id){
  try {
        const output = await fetch(`http://localhost:5000/dltsection/${id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authorization' : `${this.token}`

          },
        });

        console.log(output.status)
        if (!output.ok) {
          const errordata = await output.json();
          console.log(errordata);
          throw new Error(errordata.msg || 'An error occurred');
        }
        const data = await output.json();
        console.log(data);
        alert(data.msg);
        this.entry()

      } catch (error) {
          alert(error.msg)
      }
  },
      async reqest(id){
  try {
        const output = await fetch(`http://localhost:5000/reqest/${id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authorization' : `${this.token}`
          },
        });

        if (!output.ok) {
          const errordata = await output.json();
          throw new Error(errordata.msg || 'An error occurred');
        }

        const data = await output.json();
        alert(data.msg);
        this.entry()

      } catch (error) {
          alert(error)
      }
  },

  async retrn(id){
  try {
        const output = await fetch(`http://localhost:5000/retrn/${id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authorization' : `${this.token}`
          },
        });

        if (!output.ok) {
          const errordata = await output.json();
          throw new Error(errordata.msg || 'An error occurred');
        }

        const data = await output.json();
        alert(data.msg);
        this.entry()
      } catch (error) {
          alert(error)
      }},



        async entry() {
            try {
                const output = await fetch(`http://localhost:5000/find/0${this.find}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Authorization': `${this.token}`
          }
        });

        if (!output.ok) {
          const errordata = await output.json();
          throw new Error(errordata.msg || 'An error occurred');
        }

        const data = await output.json();
        this.sections = data.sections;
        this.books = data.books;
        

      } catch (error) {
        alert(error.msg);
      }
    }
  },
  beforeMount(){
    this.token = localStorage.getItem('token')
    this.role = localStorage.getItem('role')
    
  }




}
</script>





<style scoped>


h2{
  text-align: center;
}


.navbar {
  width: 100%;
  background-color: #007bff;
  padding: 15px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: flex-end;
}

.nav-link {
  color: #fff;
  text-decoration: none;
  font-weight: bold;
  padding: 0 15px;
  transition: color 0.3s;
  font-size: 20px;
}

.nav-link:hover {
  color: #ffdd57;
}

/* General Styles */
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f4f7f9;
  color: #333;
  margin: 0;
  padding: 0;
  padding-top: 80px; /* Space for the navbar */
}

/* Form Styles */
form {
  margin-top: 80px;
  margin: 100px auto;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

input[type="text"] {
  width: 100%;
  max-width: 400px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s ease;

}

input[type="text"]:focus {
  border-color: #3498db;
  outline: none;
}

/* Card Styles */
.card {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin: 20px auto;
  padding: 20px;
  max-width: 800px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.card h3 {
  margin: 0;
  color: #333;
  font-size: 20px;
}

.card p {
  margin: 10px 0;
  color: #666;
}

.card a {
  color: #3498db;
  text-decoration: none;
  transition: color 0.3s ease;
}

.card a:hover {
  color: #2980b9;
  text-decoration: underline;
}

/* Button Box Styles */
.button-box {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.button-box button {
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 15px;
  margin: 5px 0;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.button-box button:hover {
  background-color: #2980b9;
}

/* Different Styles for Admin and User */
[role="admin"] .card {
  border-left: 5px solid #e74c3c;
}

[role="admin"] .button-box button {
  background-color: #e74c3c;
}

[role="admin"] .button-box button:hover {
  background-color: #c0392b;
}

[role="user"] .card {
  border-left: 5px solid #2ecc71;
}

[role="user"] .button-box button {
  background-color: #2ecc71;
}

[role="user"] .button-box button:hover {
  background-color: #27ae60;
}


</style>