<template>
    <div>
      <nav class="navbar">
      <div class="nav-container">
        <RouterLink to="/AD" class="nav-link">Home</RouterLink>
        <a @click="alogout" class="nav-link">Logout</a>

      </div>
    </nav>
        <h2>Add a new section</h2>
        <form class="form" id="signUpForm" @submit.prevent>
            <div class="mb-3">
                <label for="signupName" class="form-label">Title</label>
                <input type="text" v-model="title" class="form-control" id="signupName" required>
            </div>
            <div class="mb-3">
                <label for="signupEmail" class="form-label">Date</label>
                <input type="date" v-model="date" class="form-control" id="signupEmail" required>
            </div>
            <div class="mb-3">
                <label for="signupPassword" class="form-label">Description</label>
                <input type="text" v-model="desc" class="form-control" id="signupPassword" required>
            </div>
            <button @click="entry" type="submit" class="btn btn-primary">Add Section</button>
        </form>

    </div>
</template>





    
<script>
export default {
  name: 'newsection',
  data() {
    return {
        title: '',
      date: '',
      desc: '',
      token:'',
      role:''
    };
  },
  methods: {
    alogout(){
    localStorage.clear()
      alert('You have been logged out successfully')
    this.$router.push('/adminlogin')
  },
    async entry() {
      try {
        const output = await fetch('http://localhost:5000/newsection', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authorization' : `${this.token}`

          },
          body: JSON.stringify({
            title : this.title,
            date: this.date,
            desc: this.desc
          })
        });

        if (!output.ok) {
          const errordata = await output.json();
          throw new Error(errordata.message || 'An error occurred');
        }

        const data = await output.json();
        console.log(data);
        this.$router.push('/adminsecs')
        alert(data.msg)

      } catch (error) {
          alert(error.msg)
      }
    }
  },
  beforeMount(){
    this.token = localStorage.getItem('token')
    this.role = localStorage.getItem('role')
    if (this.token) {
       if (this.role != 'admin') {
        this.$router.push('/')
         alert('Only admin can enter the site ')
       }}
    else{
      this.$router.push('/adminlogin')
      alert(' Token required to enter the site ')
    }
  }

}
</script>


<style scoped>
/* Navbar styles */
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

/* Container for the navigation links */
.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: flex-end;
}

/* Styling for navigation links */
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

/* Body styles */
body {
  background-color: #f4f4f4;
  margin: 0;
  padding-top: 60px; /* Added padding to account for the navbar height */
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

/* Container for the form and other content */
.container {
  position: relative;
  top: 0;
  left: 0;
  background-color: #ffffff;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
  width: 500px;
  padding: 30px;
  text-align: center;
  margin: 50px auto;
}

/* Header styles */
.header {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

/* Form styling */
.form {
  display: block;
  font-size: 18px;
  text-align: left;
}

/* Label styles */
.form-label {
  display: block;
  font-weight: bold;
  margin-bottom: 10px;
}

h2{
  text-align: center;
  margin-top: 70px;
}

/* Input field styling */
.form-control {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-bottom: 20px;
  transition: border-color 0.3s;
  background-color: #f5f5f5;
}

.form-control:hover {
  border-color: #007bff;
}

/* Primary button styling */
.btn-primary {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  font-size: 18px;
  cursor: pointer;
}

/* Link button styling */
.btn-link {
  text-decoration: underline;
  cursor: pointer;
  font-size: 18px;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-link:hover {
  text-decoration: underline;
}

.name {
  text-align: center;
}
</style>
