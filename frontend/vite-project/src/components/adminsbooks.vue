<template>


  <div class="container">
    <nav class="navbar">
      <div class="nav-container">
        <RouterLink to="/AD" class="nav-link">Home</RouterLink>
        <a @click="alogout" class="nav-link">Logout</a>

      </div>
    </nav>
    <div class="section-title">
      <p><strong>TITLE:</strong> {{ sdict.Title }}</p>
      <p><strong>DATE:</strong> {{ sdict.Date }}</p>
      <p><strong>DESCRIPTION:</strong> {{ sdict.Description }}</p>

    </div>
    <hr>
    <h3> Books of this Section</h3>
    <br>
    <div v-for="a in blist" :key="a.Id" class="card">
      <div class="card-content">
        <div class="card-details">
          <p><strong>TITLE:</strong> {{ a.Title }}</p>
          <p><strong>AUTHOR:</strong> {{ a.Author }}</p>
          <p><strong>AVG. REVIEW:</strong> {{ a.Rev }}</p>

          <a :href="`http://localhost:5000/book/${a.Id}.pdf`" target="_blank">Open Book</a>
        </div>
        <div class="card-actions">
          <router-link :to="`/usersnreqs/${a.Id}`" class="action-link">All Readers and Requests</router-link>
          <button @click="dltbook(a.Id)" class="action-button delete-button">Delete</button>
          <router-link :to="`/updbook/${a.Id}`" class="action-link">Update Book</router-link>
        </div>
      </div>
    </div>

    <div class="add-book">
      <router-link :to="`/newbook/${id}`" class="add-book-link">Add a new book</router-link>
    </div>
  </div>
</template>





<script>

export default {
  name: 'adminsbooks',
  
  data() {
    return {
      id: parseInt(this.$route.params.id, 10),
      blist: [],
      sdict: {},
      token: '',
      role: ''
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
        const output = await fetch(`http://localhost:5000/secbooks/${this.id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authorization': `${this.token}`
          }
        });

        if (!output.ok) {
          const errordata = await output.json();
          throw new Error(errordata.message || 'An error occurred');
        }

        const data = await output.json();
        console.log(data);
        this.sdict = data.sdict;
        this.blist = data.blist;
        console.log(this.sdict);
        console.log(this.blist);
      } catch (error) {
        alert(error.message);
      }
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
    }
  },
  beforeMount() {
    this.token = localStorage.getItem('token');
    this.role = localStorage.getItem('role');
    if (this.token) {
      if (this.role !== 'admin') {
        this.$router.push('/');
        alert('Only admin can enter the site');
      } else {
        this.entry();
      }
    } else {
      this.$router.push('/adminlogin');
      alert('Token required to enter the site');
    }
  }
};
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
    margin-top: 20px;
    padding: 0;
}

.container {
    max-width: 1000px; /* Container width */
    margin: 50px auto 0;
    padding: 20px;
}



h2 {
    text-align: center;
    margin-top: 100px;
    font-size: 2.5rem; /* Increased font size */
    color: #333; /* Darker color for better readability */
}

.section-title p {
    font-size: 1.25rem; /* Increased font size */
    color: #333; /* Darker color for better readability */
    margin-bottom: 10px; /* Add spacing between lines */
}

hr {
    border: 0;
    height: 1px;
    background: #ddd;
    margin: 20px 0; /* Add space above and below */
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
    max-width: 1200px; /* Increased maximum width of the card */
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
    gap: 10px;
    margin-top: 15px; /* Space above actions */
}

.action-link, .action-button {
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 12px 18px; /* Increased padding for larger buttons */
    text-decoration: none;
    font-size: 16px; /* Increased font size */
    cursor: pointer;
    transition: background-color 0.3s;
}

.action-link:hover, .action-button:hover {
    background-color: #0056b3;
}

.delete-button {
    background-color: #dc3545;
}

.delete-button:hover {
    background-color: #c82333;
}

.add-book {
    text-align: center;
    margin-top: 30px; /* Increased top margin */
}

.add-book-link {
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 12px 25px; /* Increased padding for a larger button */
    text-decoration: none;
    font-size: 18px; /* Increased font size */
    cursor: pointer;
    transition: background-color 0.3s;
}

.add-book-link:hover {
    background-color: #218838;
}
</style>
