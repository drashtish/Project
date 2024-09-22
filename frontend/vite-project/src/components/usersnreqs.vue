<template>
  <div>
    <nav class="navbar">
      <div class="nav-container">
        <RouterLink to="/AD" class="nav-link">Home</RouterLink>
        <a @click="alogout" class="nav-link">Logout</a>

      </div>
    </nav>
  <div class="container">
    <h1>READERS</h1>
    <div v-for="u in alist" :key="u.Id" class="card">
      <div class="card-content">
        <p><strong>Name:</strong> {{ u.Name }}</p>
        <p><strong>Email:</strong> {{ u.Email }}</p>
        <p><strong>Date of issue:</strong> {{ u.Issuedate }}</p>
        <p><strong>Due Date:</strong> {{ u.Returndate }}</p>
        <button @click="rrevoke(u.Id)" class="action-button revoke-button">Revoke Access</button>
      </div>
    </div>
    <br>
    <h4 v-if="alist.length == 0">No one is currently reading this book</h4>

<hr>
    <h1>REQUESTS</h1>
    <div v-for="u in plist" :key="u.Id" class="card">
      <div class="card-content">
        <p><strong>Name:</strong> {{ u.Name }}</p>
        <p><strong>Email:</strong> {{ u.Email }}</p>
        <button @click="approve(u.Id)" class="action-button approve-button">Approve Access</button>
        <button @click="decline(u.Id)" class="action-button decline-button">Decline Access</button>
      </div>
    </div>
    <br>
    <h4 v-if="plist.length == 0">No one requested access for this book</h4>
  </div>
  </div>
</template>





<script>
export default {
    name: 'usersnreqs',
    data() {
        return{
        id : parseInt(this.$route.params.id,10),
        plist : [],
        alist : [],
        };
    },
    methods:{
      alogout(){
    localStorage.clear()
      alert('You have been logged out successfully')
    this.$router.push('/adminlogin')
  },
    async entry(){
  try {
        const output = await fetch(`http://localhost:5000/usersnreqs/${this.id}`, {
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
        console.log(data);
        this.plist = data.plist;
        this.alist = data.alist;

      } catch (error) {
          alert(error)
      }},
      async approve(id){
  try {
        const output = await fetch(`http://localhost:5000/approve/${id}`, {
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
  async decline(id){
  try {
        const output = await fetch(`http://localhost:5000/decline/${id}`, {
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

  async rrevoke(id){
  try {
        const output = await fetch(`http://localhost:5000/rrevoke/${id}`, {
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
  }

  },
  beforeMount(){
    this.token = localStorage.getItem('token')
    this.role = localStorage.getItem('role')
    if (this.token) {
          this.entry();
      }
    else{
      this.$router.push('/')
      alert(' Token required to enter the site ')
    }
  }
}
</script>




<style scoped>


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


body {
    background-color: #f4f4f4;
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
}

.container {
    max-width: 1000px; /* Increased container width */
    margin: 50px auto 0;
    padding: 20px;
}

h1 {
    text-align: center;
    margin-top: 20px;
    font-size: 2.5rem; /* Increased font size */
    color: #333; /* Darker color for better readability */
}

p{
    font-size: 1.1rem;
}

.card {
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Increased shadow for a more pronounced effect */
    margin-bottom: 20px;
    padding: 20px;
    display: flex;
    flex-direction: column; /* Stack content vertically */
    width: 100%; /* Full width of the container */
    max-width: 800px; /* Increased maximum width of the card */
    margin: 0 auto; /* Center the card */
}

.card-content {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap; /* Allow wrapping for smaller screens */
}

.card-details {
    flex: 2;
    margin-right: 20px;
}

.card-details p {
    margin: 10px 0; /* Increased margin for better spacing */
    font-size: 1rem; /* Adjusted font size */
}

.card-actions {
    flex: 1;
    display: flex;
    justify-content: flex-end;
    gap: 1px; /* Reduced gap between buttons */
    margin-top: 15px;
}

.action-button {
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 12px 18px; /* Increased padding for larger buttons */
    text-decoration: none;
    font-size: 16px; /* Increased font size */
    cursor: pointer;
    transition: background-color 0.3s;
    margin-right: 10px;
}

.action-button:hover {
    background-color: #0056b3;
}

.revoke-button {
    background-color: #dc3545;
}

.revoke-button:hover {
    background-color: #c82333;
}

.approve-button {
    background-color: #28a745;
}

.approve-button:hover {
    background-color: #218838;
}

.decline-button {
    background-color: #ffc107;
}

.decline-button:hover {
    background-color: #e0a800;
}
</style>