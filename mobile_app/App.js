import React, {useState} from 'react';
import { StyleSheet, Text, View, TextInput, Button, Alert } from 'react-native';

const API_URL = 'http://10.0.2.2:8000'; // Android emulator; use http://localhost:8000 for web

export default function App() {
  const [phone,setPhone]=useState('');
  const [password,setPassword]=useState('');
  const [token,setToken]=useState('');
  const [balance,setBalance]=useState(null);

  const register = async ()=>{
    try{
      const res = await fetch(API_URL + '/auth/register',{
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({phone, password})
      });
      const data = await res.json();
      if(res.ok) Alert.alert('Registered');
      else Alert.alert('Error', JSON.stringify(data));
    }catch(e){Alert.alert('Error', e.message)}
  };

  const login = async ()=>{
    try{
      const body = new URLSearchParams();
      body.append('username', phone);
      body.append('password', password);
      const res = await fetch(API_URL + '/auth/token',{
        method:'POST', headers:{'Content-Type':'application/x-www-form-urlencoded'},
        body: body.toString()
      });
      const data = await res.json();
      if(res.ok){ setToken(data.access_token); Alert.alert('Logged in'); }
      else Alert.alert('Login error', JSON.stringify(data));
    }catch(e){Alert.alert('Error', e.message)}
  };

  const getBalance = async ()=>{
    try{
      const res = await fetch(API_URL + '/wallet/balance?phone=' + encodeURIComponent(phone),{
        method:'GET', headers: {'Authorization': 'Bearer ' + token}
      });
      const data = await res.json();
      if(res.ok) setBalance(data.balance);
      else Alert.alert('Error', JSON.stringify(data));
    }catch(e){Alert.alert('Error', e.message)}
  };

  return (
    <View style={styles.container}>
      <Text style={{fontWeight:'bold', marginBottom:10}}>FinLynq Mobile Demo</Text>
      <TextInput style={styles.input} placeholder="phone" value={phone} onChangeText={setPhone} />
      <TextInput style={styles.input} placeholder="password" value={password} onChangeText={setPassword} secureTextEntry />
      <View style={{flexDirection:'row'}}>
        <Button title="Register" onPress={register} />
        <View style={{width:8}} />
        <Button title="Login" onPress={login} />
      </View>
      <View style={{height:12}} />
      <Button title="Get Balance" onPress={getBalance} />
      {balance !== null && <Text style={{marginTop:16}}>Balance: {balance}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container:{flex:1, padding:20, justifyContent:'center'},
  input:{borderWidth:1, padding:8, marginBottom:8}
});
