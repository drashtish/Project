<template>
  <div>
    <nav class="navbar">
      <div class="nav-container">
        <RouterLink to="/UD" class="nav-link">Home</RouterLink>
        <a @click="ulogout" class="nav-link">Logout</a>

      </div>
    </nav>

    <div class="content">
      <h3>Title :  {{ this.sdict.Title }}</h3>
      <h3>Date of Creation :  {{ this.sdict.Date }}</h3>
      <h3>Description :  {{ this.sdict.Description }}</h3>
      <hr>
      <br>
      <h2>All Books of this Section</h2>

      <div class="books-list">
        <div class="book-item" v-for="a in blist" :key="a.Id">
          <h4>Title: {{ a.Title }}</h4>
          <p>Author: {{ a.Author }}</p>

          <p v-if="a.Status == 'Pending'" class="status-pending">
            Your request is not yet Approved, Please wait !
          </p>

          <p v-else-if="a.Status == 'Approved'" class="status-approved">
            Date of Issue: {{ a.Issuedate }}<br>
            Due Date: {{ a.Duedate }}<br>
            <a :href="`http://localhost:5000/book/${a.Id}.pdf`" target="_blank">Open Book</a>
            <button @click="goToReviewPage(a.Id)" class="btn-review">Leave a Review</button>
            <button @click="retrn(a.Id)" class="btn-return">Return Book</button>
          </p>

          <p v-else-if="a.Status == 'Rejected'" class="status-rejected">
            Sorry to say that, Your request is Rejected !
          </p>

          <p v-else class="status-request">
            Request this book to read
            <button @click="reqest(a.Id)" class="btn-request">Request</button>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>







<script>
export default {
  name: 'usersbooks',
  data() {
  return{
    id: parseInt(this.$route.params.id,10),
    blist : [],
    sdict : {},
    token: '',
    role:''
  };},
  methods: {
    ulogout(){
    localStorage.clear()
      alert('You have been logged out successfully')
    this.$router.push('/')
  },
    goToReviewPage(bookId) {
      this.$router.push(`/review/${bookId}`);
    },
  async entry(){
  try {
        const output = await fetch(`http://localhost:5000/secbooks/${this.id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authorization' : `${this.token}`
          },
        });
        console.log(output.status)
        console.log(output)


        if (!output.ok) {
          const errordata = await output.json();
          throw new Error(errordata.message || 'An error occurred');
        }

        const data = await output.json();
        console.log(data);
        this.sdict = data.sdict;
        this.blist = data.blist;
        console.log(this.sdict);
        console.log(this.blist)
      } catch (error) {
          alert(error)
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
      }}



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
  font-size: 20px;
}

.nav-link:hover {
  color: #ffdd57;
}


/* Content */
.content {
  max-width: 800px;
  margin: 50px auto 0; /* Adjusted for fixed navbar */
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
}

/* Books List */
.books-list {
  margin-top: 20px;
}

.book-item {
  background-color: #f9f9f9;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.book-item h4 {
  font-size: 20px;
  color: #007bff;
}

.book-item p {
  font-size: 16px;
}

.status-pending {
  color: #ffc107;
}

.status-approved {
  color: #28a745;
}

.status-rejected {
  color: #dc3545;
}

.status-request {
  color: #6c757d;
}

.btn-review, .btn-return, .btn-request {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 15px;
  margin-top: 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-review:hover, .btn-return:hover, .btn-request:hover {
  background-color: #0056b3;
}
</style>
