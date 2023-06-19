import { useState } from 'react';

const user = {
	firstName: 'Jane',
	lastName: 'Jacobs'
}

function CreateInput({userData, setUserData, isEdit, label, value }) { 	

	return (
		isEdit ? 
			<label>
				<span>{label}</span>
				<input 
					type="text" 
					defaultValue={userData[value]} 
					onChange={ (e) => {setUserData({...userData, [value]: e.target.value}) }}           
				/>
			</label>
			:
			<p>{label} {userData[value]}</p>
	)
}

function CreateButton({ isEdit, setIsEdit }) {

	return (
		<button type="submit" onClick={ ()=> setIsEdit(!isEdit)}>
			{isEdit ? 'Save Profile' : 'Edit Profile'}
		</button>
	)
}

function App() {	

	const [userData, setUserData] = useState(user)	
	const [isEdit, setIsEdit] = useState(true)

	return (
	   <form onSubmit={ (e) => e.preventDefault() } >
			<CreateInput 
				userData={userData} 
				setUserData={setUserData} 
				isEdit={isEdit} 
				label='First name: ' 
				value='firstName'
			/>
			<CreateInput 
				userData={userData} 
				setUserData={setUserData} 
				isEdit={isEdit} 
				label='Last name: ' 
				value='lastName'/>
			<CreateButton 
				isEdit={isEdit} 
				setIsEdit={setIsEdit} 
			/>
			<p><i>Hello, {userData.firstName} {userData.lastName}!</i></p>
	   </form>
	);
}

export default App;
