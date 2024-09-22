<template>
  <div class="container">
    <nav class="navbar">
      <a href="/profile" class="nav-link">Your Profile</a>
      <RouterLink to="/searchsec" class="nav-link">Search</RouterLink> 
      <a @click="ulogout" class="nav-link">Logout</a>
    </nav>
    <br>
    <br>
    <h1 class="greeting">Hello User</h1>
    <hr class="divider">

    <h2 class="greeting">All Sections</h2>

    <div class="sections">
      <h3 v-for="a in sec" :key="a.Id" class="section-link">
        <router-link :to="`/usersbooks/${a.Id}`">{{ a.Title }}</router-link>
      </h3>
    </div>
  </div>
</template>



<script>
     export default {
    name: 'UD',
    data() {
      return {
        token: '',
        role: '',
        sec : []
      }
    },
  
  methods:{
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
          throw new Error(errordata.msg || 'An error occurred');
        }

        this.sec = await output.json();
        console.log(this.sec);
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
  ulogout(){
    localStorage.clear()
      alert('You have been logged out successfully')
    this.$router.push('/')
  },

  },
  beforeMount(){
    this.token = localStorage.getItem('token')
    this.role = localStorage.getItem('role')
    if (this.token) {
          this.entry();
          this.auto_revoke()
    }  
    else{
      this.$router.push('/')
      alert(' Token required to enter the site ')
    }
  }}


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
  display: flex;
  justify-content: flex-end;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: flex-end; /* Aligns the nav links to the right */
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
.content {
  max-width: 800px;
  margin: 120px auto 0; /* Adjusted for fixed navbar */
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
}

/* Greeting and Divider */
.greeting {
  text-align: left;
  color: #444;
  font-size: 28px;
  margin-bottom: 20px;
}

.divider {
  border: 0;
  height: 1px;
  background: #ddd;
  margin-bottom: 20px;
}

/* Sections */
.sections {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.section-link {
  background-color: #f1f1f1;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s, box-shadow 0.3s;
}

.section-link a {
  text-decoration: none;
  color: #007bff;
  font-size: 20px;
  font-weight: bold;
}

.section-link:hover {
  background-color: #e6f2ff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}
</style>
