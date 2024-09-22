<template>

    <div class="container">
      
        <h2>Sign Up</h2>
        <form class="form" id="signUpForm" @submit.prevent>
            <div class="mb-3">
                <label for="signupName" class="form-label">Name</label>
                <input type="text" v-model="name" class="form-control" id="signupName" name="name" required>
            </div>
            <div class="mb-3">
                <label for="signupEmail" class="form-label">Email</label>
                <input type="email" v-model="email" class="form-control" id="signupEmail" name="email" required>
            </div>
            <div class="mb-3">
                <label for="signupPassword" class="form-label">Password</label>
                <input type="password" v-model="password" class="form-control" id="signupPassword" name="password" required>
            </div>
            <div class="mb-3">
                <label for="signupcheck" class="form-label">Details are correctly filled</label>
                <input type="checkbox" class="form-control" id="signupcheck" name="check" required>
            </div>
            <button @click="entry" type="submit" class="btn btn-primary">Register</button>
        </form>
        Already have an account? <a href="/">Login</a>
    </div>
</template>


<script>
export default {
  name: 'register',
  data() {
    return {
        name: '',
      email: '',
      password: ''
    };
  },
  methods: {
    async entry() {
      try {
        const output = await fetch('http://localhost:5000/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'

          },
          body: JSON.stringify({
            name : this.name,
            email: this.email,
            password: this.password
          })
        });

        if (!output.ok) {
          const errordata = await output.json();
          throw new Error(errordata.message || 'An error occurred');
        }

        const data = await output.json();
        console.log(data);
        this.$router.push('/')
        alert(data.msg)

      } catch (error) {
          alert(error.msg)
      }
    },
    
  }
}
</script>



<style scoped>
        body {
            align-items: center;
            justify-content: center;
            height: 100vh;
            background-color: #f4f4f4;
            margin: 0;
        }
    
        .container {
            position: absolute;
            top: 50%;
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

        .name{
            text-align: center;
        }

    

      
    </style>
    
