import { useState } from 'react';


function App() {
	
	const user = {
		firstName: 'Jane',
		lastName: 'Jacobs'
	 }

	const [isEdit, setIsEdit] = useState(true)
	const [userData, setUserData] = useState(user)
	
	function CreateInput({label, value}) { 
	  
	  return (
		 isEdit ? 
			  <label>
				  <span>{label}</span>
				  <input 
						type="text" 
						defaultValue={userData[value]} 
						onChange={ 
							(e) => {setUserData({...userData, [value]: e.target.value})
							console.log(userData)
							console.log(e.target.value)}
						}           
				 />
			  </label>
			:
			<p>{label} {userData[value]}</p>
		 )
	}
 
	function CreateButton() {
	  return (
		 <button type="submit" onClick={ ()=> setIsEdit(!isEdit)}>
			{isEdit ? 'Save Profile' : 'Edit Profile'}
		 </button>
	  )
	}
	return (
	  <form onSubmit={ (e) => e.preventDefault() } >
		 <CreateInput label='First name: ' value='firstName'/>
		 <CreateInput label='Last name: ' value='lastName'/>
		 <CreateButton />
		 <p><i>Hello, {userData.firstName} {userData.lastName}!</i></p>
	  </form>
	);
}

export default App;
