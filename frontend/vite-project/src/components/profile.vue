<template>
  <div>
    <nav class="navbar">
      <div class="nav-container">
        <RouterLink to="/UD" class="nav-link">Home</RouterLink>
        <a @click="ulogout" class="nav-link">Logout</a>
      </div>
    </nav>
    
    <div class="profile-content">
      <h1 class="profile-heading">YOUR PROFILE</h1>
      
      <p class="profile-info">NAME : {{ name }}</p>
      <p class="profile-info">EMAIL : {{ email }}</p>
      
      <h2 class="section-heading">Books Details</h2>
      
      <div class="books-list">
        <div v-for="a in data" :key="a.Id" class="book-item">
          <div class="book-detail"><span class="book-title">TITLE:</span> {{ a.Title }}</div>
          <div class="book-detail"><span class="book-title">AUTHOR:</span> {{ a.Author }}</div>
          <div class="book-detail"><span class="book-title">DATE OF ISSUE:</span> {{ a.IssueDate }}</div>
          <div class="book-detail"><span class="book-title">DUE DATE:</span> {{ a.ReturnDate }}</div>
          
          <a :href="`http://localhost:5000/book/${a.Id}.pdf`" target="_blank" class="btn-link">Open Book</a>
          <button @click="goToReviewPage(a.Id)" class="btn-review">Leave a Review</button>
          <button @click="retrn(a.Id)" class="btn-return">Return Book</button>
        </div>
      </div>
    </div>
  </div>
</template>













<script>
export default {
  name: 'profile',
  data(){
    return{
        data :[],
        token: '',
        role:'',
        name:'',
        email:''
    };
  },
  methods: {
    ulogout(){
    localStorage.clear()
      alert('You have been logged out successfully')
    this.$router.push('/')
  },
    goToReviewPage(bookId) {
      this.$router.push(`/review/${bookId}`);
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
        const output = await fetch(`http://localhost:5000/profile`, {
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
        this.data = data.data,
        this.name = data.Name,
        this.email = data.Email
        } catch (error) {
        alert(error.msg);
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
  font-size: 18px;
}

.nav-link:hover {
  color: #ffdd57;
}

/* Profile Page */
.profile-content {
  margin-top: 80px; /* Adjusted for fixed navbar */
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
  background-color: #f4f4f4;
}

.profile-heading {
  font-size: 28px;
  font-weight: 700;
  color: #007bff;
  margin-bottom: 20px; /* Reduced gap */
  text-align: center;
  border-bottom: 2px solid #007bff;
  padding-bottom: 10px;
}

.section-heading {
  font-size: 24px;
  font-weight: 600;
  color: #444;
  margin-bottom: 15px; /* Reduced gap */
  border-bottom: 1px solid #ddd;
  padding-bottom: 8px;
}

.book-item {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.book-detail {
  margin-bottom: 10px;
}

.book-title {
  font-weight: 600;
  color: #007bff;
}

a.btn-link {
  color: #007bff;
  text-decoration: none;
  font-size: 16px;
  display: block;
  margin-bottom: 10px;
}

a.btn-link:hover {
  text-decoration: underline;
}

.btn-review, .btn-return {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px 15px;
  font-size: 16px;
  cursor: pointer;
  margin-right: 10px;
  transition: background-color 0.3s;
}

.btn-review:hover, .btn-return:hover {
  background-color: #0056b3;
}

.btn-return {
  background-color: #28a745;
}

.btn-return:hover {
  background-color: #218838;
}
</style>