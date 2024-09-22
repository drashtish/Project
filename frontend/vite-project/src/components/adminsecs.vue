<template>
  <div>
    <nav class="navbar">
      <div class="nav-container">
        <RouterLink to="/AD" class="nav-link">Home</RouterLink>
        <a @click="alogout" class="nav-link">Logout</a>

      </div>
    </nav>
    <h2>All Sections</h2>
    <div v-for="a in sec" :key="a.Id" class="card">
      <div class="card-content">
        <div class="card-title">
          <router-link :to="`/adminsbooks/${a.Id}`">{{ a.Title }}</router-link>
        </div>
        <div class="card-actions">
          <router-link :to="`/updsection/${a.Id}`" class="action-link">Update Section</router-link>
          <button @click="dlt(a.Id)" class="action-button">Delete</button>
        </div>
      </div>
    </div>
    <div class="add-section">
      <RouterLink to="/newsection" class="add-section-link">Add a new section</RouterLink>
    </div>
  </div>
</template>




<script>

export default {
  name: 'adminsecs',
  
  data() {
  return{
    sec : [],
    token: '',
    role:''
  };},

  methods: {
    alogout(){
    localStorage.clear()
      alert('You have been logged out successfully')
    this.$router.push('/adminlogin')
  },
  async entry(){
  try {
        const output = await fetch('http://localhost:5000/allsections', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authorization' : `${this.token}`

          },
        });

        if (!output.ok) {
          const errordata = await output.json();
          throw new Error(errordata.message || 'An error occurred');
        }

        this.sec = await output.json();
        console.log(this.sec);
      } catch (error) {
          alert(error.msg)
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

        if (!output.ok) {
          const errordata = await output.json();
          throw new Error(errordata.msg || 'An error occurred');
        }

        const data = await output.json();
        alert(data.msg);
        this.entry();

      } catch (error) {
          alert(error.msg)
      }
  },

  },
  beforeMount(){
    this.token = localStorage.getItem('token')
    this.role = localStorage.getItem('role')
    if (this.token) {
       if (this.role != 'admin') {
        this.$router.push('/')
         alert('Only admin can enter the site ')
       }
      else {
          this.entry();
      }}
    else{
      this.$router.push('/adminlogin')
      alert(' Token required to enter the site ')
    }
  }
}
</script>


<style scoped>
/* Navbar */
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

/* Page Content */
body {
    background-color: #f4f4f4;
    font-family: Arial, sans-serif;
}

/* Ensure content starts below the navbar */
h2 {
    text-align: center;
    margin-top: 70px; /* Adjusted to ensure content is fully visible */
}

.card {
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    margin: 20px auto;
    padding: 20px;
    width: 80%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card-content {
    display: flex;
    justify-content: space-between;
    width: 100%;
}

.card-title {
    font-size: 20px;
    font-weight: bold;
}

.card-title a {
    text-decoration: none;
    color: #007bff;
}

.card-title a:hover {
    text-decoration: underline;
}

.card-actions {
    display: flex;
    gap: 10px;
}

.action-link, .action-button {
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 15px;
    text-decoration: none;
    font-size: 14px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.action-link:hover, .action-button:hover {
    background-color: #0056b3;
}

.action-button {
    background-color: #dc3545;
}

.action-button:hover {
    background-color: #c82333;
}

.add-section {
    text-align: center;
    margin-top: 20px;
}

.add-section-link {
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    text-decoration: none;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.add-section-link:hover {
    background-color: #218838;
}
</style>
