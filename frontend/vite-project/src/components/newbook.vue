<template>
  <div>
    <nav class="navbar">
      <div class="nav-container">
        <RouterLink to="/AD" class="nav-link">Home</RouterLink>
        <a @click="alogout" class="nav-link">Logout</a>

      </div>
    </nav>
  <h2>Add a new book</h2>
  <form class="form" id="signUpForm" @submit.prevent="entry">
    <div class="mb-3">
      <label for="signupName" class="form-label">Title</label>
      <input type="text" v-model="title" class="form-control" id="signupName" required>
    </div>
    <div class="mb-3">
      <label for="signupAuthor" class="form-label">Author</label>
      <input type="text" v-model="author" class="form-control" id="signupAuthor" required>
    </div>
    <div>
      Upload File
      <input type="file" @change="addFile" required>
    </div><br>
    <button type="submit" class="btn btn-primary">Add Book</button>
  </form>
  </div>
</template>

<script>
export default {
  name: 'NewBook',
  data() {
    return {
      id: this.$route.params.id,
      title: '',
      author: '',
      file: null,
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
      const bookDetails = new FormData();
      bookDetails.append('Title', this.title);
      bookDetails.append('Author', this.author);
      if (this.file) {
        bookDetails.append('File', this.file);
      }

      try {
        const response = await fetch(`http://localhost:5000/newbook/${this.id}`, {
          method: 'POST',
          body: bookDetails,
          headers: {
            'Authorization' : `${this.token}`
          }
        });

        console.log('Response status:', response.status);
        console.log('Response type:', response.headers.get('content-type'));

        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
          const data = await response.json();
          console.log(data);
          this.$router.push(`/adminsbooks/${this.id}`);
          alert(data.msg);
        } else {
          const text = await response.text();
          console.error('Unexpected response:', text);
          alert('Unexpected response from the server');
        }
      } catch (error) {
        console.error('Fetch error:', error);
        alert(error.message);
      }
    },
    addFile(event) {
      this.file = event.target.files[0];
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

h2{
  text-align: center;
  margin-top: 70px;
}

  body {
    align-items: center;
    justify-content: center;
    height: 100vh;
    background-color: #f4f4f4;
    margin: 0;
  }

  .container {
    position: absolute;
    top: 90%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #ffffff;
    border: 1px solid #ccc;
    border-radius: 10px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
    width: 500px;
    padding: 30px;
    text-align: center;
  }

  .header {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
  }

  .form {
    display: block;
    font-size: 18px;
    text-align: left;
  }

  .form-label {
    display: block;
    font-weight: bold;
    margin-bottom: 10px;
  }

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

  .btn-primary {
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 18px;
    cursor: pointer;
  }

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
