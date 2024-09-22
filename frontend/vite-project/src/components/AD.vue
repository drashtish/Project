<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar">
      <div class="nav-container">
        <RouterLink to="/searchsec" class="nav-link">Search</RouterLink>
        <a @click="alogout" class="nav-link">Logout</a>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="content">
      <h1 class="greeting">Hello Admin</h1>

      <!-- Statistics Display -->
      <div class="stats-container">
        <div class="stat-box">
          Total Users<br>
          {{ users }}<br>
        </div>

        <div class="stat-box">
          Total Books <br>
          {{ books }}<br>
        </div>

        <div class="stat-box">
          Total Sections <br>
          {{ sections }}<br>
          <RouterLink to="/adminsecs" class="nav-link-inline">View all Sections</RouterLink>
        </div>
      </div>

     

      <!-- Graphs Section -->
      <div class="graphs-container">
        <h1>Graphs</h1>
        <div class="graphs-row">
          <img src="../../public/section_books_pie_chart.png" alt="Section Books Pie Chart" class="graph-image"/>          
          <img src="../../public/violin_requests.png" alt="Section Books Pie Chart" class="graph-image"/>          
        </div>
      </div>



       <!-- Export CSV Button -->
       <div class="export-container">
        <h1><i>Get all data in CSV format:</i></h1>
        <button @click='export_csv' class="export-button">Export CSV</button>
      </div>
    </div>
  </div>
</template>





<script>

export default {
  name: 'AD',
  
  data() {
  return{
    users:0,
    sections:0,
    books:0,
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
        const output = await fetch('http://localhost:5000/allinfo', {
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

        const data = await output.json();
        this.users = data.users,
        this.sections = data.sections,
        this.books = data.books
      } catch (error) {
          alert(error.msg)
      }
  },

  async auto_revoke(){
  try {
        const output = await fetch('http://localhost:5000/auto_revoke', {
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

        if ( output.status == 201){
        const data = await output.json();
        alert(data.msg)
        }

      } catch (error) {
          alert(error.msg)
      }
  },

  async export_csv(){
  try {
        const output = await fetch('http://localhost:5000/export_csv', {
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
        alert(data.msg)

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
          this.auto_revoke();
      }}
    else{
      this.$router.push('/adminlogin')
      alert(' Token required to enter the site ')
    }
  }
}
</script>



<style scoped>


.button {
  background-color: #007bff; /* Blue background */
  border: none; /* Remove borders */
  color: white; /* White text */
  padding: 12px 20px; /* Some padding */
  text-align: center; /* Center the text */
  text-decoration: none; /* Remove underline */
  display: inline-block; /* Make the button inline */
  font-size: 16px; /* Increase font size */
  margin: 10px 2px; /* Add some margin */
  cursor: pointer; /* Add a pointer on hover */
  border-radius: 5px; /* Rounded corners */
  transition: background-color 0.3s ease; /* Smooth transition for hover */
}

.button:hover {
  background-color: #0056b3; /* Darker blue background on hover */
}

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
  padding: 0 20px;
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




/* Graphs Section Styles */
.graphs-container {
  margin-top: 50px;
}

.graphs-container h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

.graphs-row {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 30px;
}

.graph-image {
  max-width: 45%;
  height: auto;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* Inline Navigation Links */
.nav-link-inline {
  color: #007bff;
  text-decoration: none;
  font-weight: bold;
  margin-top: 10px;
  display: inline-block;
}

.nav-link-inline:hover {
  color: #0056b3;
}

/* Page Content */
.content {
  max-width: 800px;
  margin: 80px auto 0; /* Adjusted for fixed navbar */
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
}

/* Greeting and Divider */
.greeting {
  text-align: center;
  color: #444;
  font-size: 28px;
  margin-bottom: 20px;
}

/* Stats Boxes */
.stats-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 20px;
}

.stat-box {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  text-align: center;
  width: 300px;
  height: 70px;
  font-size: 20px;
}
</style>
