import React, {useEffect, useState} from "react";
import {useNavigate, useParams} from "react-router-dom";
import axios from "axios";
import { io, Socket } from 'socket.io-client';

interface DATA {
    cid : string ;

}

export default function Track() {
    const {cid} = useParams();
    const [name, setName] = useState("");
    const [status, setStatus] = useState(0);
    const [hos, setHos] = useState("");
    const [am, setAm] = useState("");
    const [nhs, setNhs] = useState("");
    const [dob, setDob] = useState("");
    const [address, setAddress] = useState("");
    const [medical, setMedical] = useState("");
    const [injury, setInjury] = useState("");
    const [gender, setGender] = useState("");
    const [age, setAge] = useState("");
    const [time, setTime] = useState("");
    const [action, setAction] = useState("");
    const [allergies, setAllergies] = useState("");
    const navigate = useNavigate();

    useEffect(()=>{

        let id = cid!.toString();

        axios.get(`/api/get/${cid}`).then((res) => res.data).then(
            (data)=>{
                console.log(data)
                setName(data['pname']);
                setStatus(data['status']);
                setHos(data['hospital']);
                setAm(data['a_num']);
                console.log(data['nhs']);
                axios.get(`http://localhost:8080/get/${data['nhs']}`).then((res) => res.data).then(
                    pat =>{
                        setNhs(pat['nhs']);
                        setAction(pat['action_taken']);
                        setAddress(pat['address']);
                        setAge(pat['age']);
                        setAllergies(pat['allergies']);
                        setDob(pat['dob']);
                        setGender(pat['gender']);
                        setInjury(pat['injury']);
                        setMedical(pat['medical']);
                        setTime(pat['time']);
                    }
                ).catch(e => console.log(e))

            }
        );
    });

    return (

        <div className="page">
            <link rel="stylesheet"
                  href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"/>
            <div style={{padding: 30, borderRadius: 23}}>
                <div style={{
                    flex: 2,
                    display: 'flex',
                    width: 'auto',
                    justifyContent: "center",
                    alignItems: 'center',
                    alignContent: 'center',
                    flexWrap: 'wrap',
                    order: 2,
                    flexDirection: 'row'
                }}>



                </div>
            </div>


            <div style={{padding: 30, borderRadius: 23}}>
                <div style={{
                    flex: 2,
                    display: 'flex',

                    width: 'auto',
                    justifyContent: "center",
                    alignItems: 'center',
                    alignContent: 'center',
                    flexWrap: 'wrap',
                    order: 2,
                    flexDirection: 'row'
                }}>
                    <div style={{
                        borderRadius: 12,
                        background: 'rgba(255,255,255,0.18)',
                        height: 180,
                        padding: '20px',
                        margin: '20px',
                        alignContent: 'center',
                        boxShadow: "4px 4px 16px 10px rgba(110,110,110,0.09) "
                    }} className='wrap-text-white shGreen'>
                        <div style={{display: 'flex', width: '100%', justifyContent: 'center', alignContent: 'center'}}>

                            <span className="material-symbols-outlined grayx" style={{color: '#ffd689', fontSize: 64}}>
                                        person
                                    </span>
                        </div>
                        <p style={{color: '#b1b0b0'}}>{name}</p>

                    </div>

                    <div style={{
                        borderRadius: 12,
                        background: 'rgba(255,255,255,0.18)',
                        height: 180,
                        padding: '20px',
                        margin: '20px',
                        alignContent: 'center',
                        boxShadow: "4px 4px 16px 10px rgba(110,110,110,0.09) "
                    }} className='wrap-text-white shGreen'>
                        <div style={{display: 'flex', width: '100%', justifyContent: 'center', alignContent: 'center'}}>

                            <span className="material-symbols-outlined grayx" style={{color: '#ff8989', fontSize: 64}}>
                                        church
                                    </span>
                        </div>
                        <p style={{color: '#a8a8a8'}}>{hos}
                            </p>

                    </div>

                    <div style={{
                        borderRadius: 12,
                        background: 'rgba(255,255,255,0.18)',
                        height: 180,
                        padding: '20px',
                        margin: '20px',
                        alignContent: 'center',
                        boxShadow: "4px 4px 16px 10px rgba(110,110,110,0.09) "
                    }} className='wrap-text-white shGreen'>
                        <div style={{display: 'flex', width: '100%', justifyContent: 'center', alignContent: 'center'}}>

                            <span className="material-symbols-outlined grayx" style={{color: '#7bef93', fontSize: 64}}>
                                        pin
                                    </span>
                        </div>
                        <p style={{color: '#a8a8a8'}}>{am}</p>

                    </div>

                </div>
            </div>

            <div style={{
                background: 'rgb(250,250,250,1.0    )',
                height: '80%',
                margin:'auto',
                width: '80%',
                maxHeight: 380,
                maxWidth: 1050,
                minWidth: 300,
                minHeight: 250,
                borderRadius: 30,
                boxShadow: '4px 4px 16px 10px rgba(110,110,110,0.09)',
                overflow: 'auto'
            }} className="shadow-container">

                <div style={{padding: '20px', textAlign: 'center', justifyContent: 'center'}}>
                    <div style={{display: 'flex'}}>
                        <button className='circle'
                                style={{background: 'transparent', width: 'auto', height: 'auto', margin: 0}}
                                onClick={() => {
                                }}>

                        </button>
                        <button className='circle'
                                style={{background: 'transparent', width: 'auto', height: 'auto', margin: 0}}
                                onClick={() => {
                                }}>
                                    <span className="material-symbols-outlined" style={{color: '#b96a6a'}}>
                                        ambulance
                                    </span>
                        </button>
                    </div>

                    <form onSubmit={(e) => {
                        let action_taken = (document.getElementById('task') as HTMLInputElement).value;
                        const data: FormData = new FormData();
                        data.append('nhs', nhs);
                        data.append('action_taken', action_taken);
                        data.append('dob', dob);
                        data.append('name', name);
                        data.append('medical', medical);
                        data.append('address', address);
                        data.append('allergies', allergies);
                        data.append('gender', gender);
                        data.append('injury', injury);
                        data.append('timestamp', time);
                        data.append('age', age);
                        data.append('hospital_code', hos);


                        axios.post(`http://localhost:8080/update/${nhs}`, data, {
                            headers: {
                                'Content-Type': 'multipart/form-data',
                            },
                        }).then(
                            response => {

                                if (response.data === "Successful Update") {
                                    axios.get(`/api/updateStatus/${cid}`).then(response => { navigate('/cases')}).catch(error => {alert("error status")})

                                } else {
                                    alert("error")
                                }
                            }
                        ).catch(error => {
                            alert(error)
                        })

                    }}>
                        <div style={{display: 'flex', alignItems: 'center', marginLeft: 26}}>
                            <span style={{marginLeft: 20}}>
                                {injury}
                            </span>

                            <span style={{marginLeft: 20}}>
                                {time}
                            </span>

                            <span style={{marginLeft: 20}}>
                                {medical}
                            </span>
                        </div>

                        <div style={{display: 'flex', alignItems: 'center', marginLeft: 26}}>
                                    <span style={{color: '#aaa', fontSize: 19, marginRight: 10}}
                                          className="material-symbols-outlined">
                                         task
                                    </span><p style={{color: '#aaa', fontSize: 14}}>Action Taken</p>
                        </div>
                        <input placeholder='@applied CPR' className='noner' id="task"/>
                        <br/>

                        <button className='redx shRed' type="submit" style={{
                            margin: 20,
                            width: 170,
                            paddingTop: 8,
                            paddingBottom: 8
                        }}>Log as transported
                        </button>
                    </form>
                </div>

            </div>

        </div>
    );
}