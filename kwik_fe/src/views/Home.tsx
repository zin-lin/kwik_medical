import React, {useEffect, useRef, useState} from "react";
import {Link, useNavigate} from "react-router-dom";
import promo from '../assets/ad.png';
import Login from "./Login";
export default function Home (){

    const reader = new FileReader();
    //reader.readAsText('../.anx');
    const [data, setData] = useState('');
    useEffect(() => {
        var res = fetch('.anx');
        res.then(res => res.text()).then(data => setData(data));
        console.log(data);

    })

    const navigate = useNavigate();

    return (
        <div className='page'>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
            <div style={{padding: 50}}>

                <div>
                    <img src={promo} style={{width:'100%', paddingBottom:0}}/>
                </div>

                <div style={{padding:60}}>
                    <button className='redx shRed' style={{width:'300px'}} onClick={()=>{
                        navigate('/add-case');
                    }}>
                        <p>Report Emergency Now</p>
                    </button>
                </div>

                <div style={{
                    zIndex: 9,
                    height: 'auto',
                    background: 'rgba(255,255,255,0.32)',
                    marginTop: -2,
                    borderRadius:23,
                    position: 'relative',
                    boxShadow: "4px 4px 16px 7px rgba(130,130,130,0.16) ",
                }} className='glassed'>
                    <div className='glassed' style={{padding:30, borderRadius:23}}>
                        <div style={{
                            flex: 2,
                            display: 'flex',
                            height: 'auto',
                            width: 'auto',
                            justifyContent: "center",
                            flexWrap: 'wrap',
                            order: 2,
                            flexDirection: 'row'
                        }}>
                            <div style={{
                                borderRadius: 12,
                                background: '#e2ffe1',
                                height: '100%',
                                padding: '20px',
                                margin: '20px',
                                boxShadow: "4px 4px 16px 10px rgba(110,110,110,0.09) "
                            }} className='wrap-text-white shGreen'>
                                <div style={{display: 'flex'}}>
                                    <div className='circle' style={{background: 'grey'}}></div>
                                    <div className='circle bluex' style={{width: 60, height: 13}}></div>
                                    <span className="material-symbols-outlined grayx">
                                        map
                                    </span>
                                </div>
                                <p style={{color: '#555'}}>"Seamless map access in applications helps locate medical
                                    services quickly, optimizing routes for emergency responders and ensuring timely assistance, ultimately enhancing healthcare accessibility and response efficiency during emergencies.
                                    "</p>
                                <button className='redx shRed'>Loate Now</button>
                            </div>
                                <div style={{
                                    borderRadius: 12,
                                    background: '#e2ffff',
                                    height: '100%',
                                    padding: '20px',
                                    margin: '20px',
                                    boxShadow: "4px 4px 16px 10px rgba(110,110,110,0.09) "
                                }} className='wrap-text-white'>
                                    <div style={{display: 'flex'}}>
                                        <div className='circle' style={{background: 'grey'}}></div>
                                        <div className='circle'
                                             style={{background: 'orange', width: 60, height: 12}}></div>
                                        <span className="material-symbols-outlined grayx">
                                            call
                                        </span>
                                    </div>
                                    <p style={{color: '#555'}}>" Ambulances provide rapid transportation and immediate
                                        medical care, bridging the gap between emergency scenes and hospitals, ensuring prompt treatment that can significantly improve patient survival and outcomes.

                                    "</p>
                                <button className='orangex shOrange'>Save Lives</button>
                            </div>
                            <div style={{
                                borderRadius: 12,
                                background: '#ffe6e6',
                                height: '100%',
                                padding: '20px',
                                margin: '20px',
                                boxShadow: "4px 4px 16px 10px rgba(130,130,130,0.15) "
                            }} className='wrap-text-white'>
                                <div style={{display: 'flex'}}>
                                    <div className='circle' style={{background: 'grey'}}></div>
                                    <div className='circle redx' style={{width: 60, height: 13}}></div>
                                    <span className="material-symbols-outlined grayx">
                                        ambulance
                                    </span>
                                </div>
                                <p style={{color: '#555'}}>" NHS ambulance services ensure equal access to emergency
                                    care, supporting public health and well-being in the United Kingdom by providing free, life-saving services, reinforcing the NHS’s commitment to accessible healthcare for all."</p>
                                <button className='shPurple purplex'>Ambulance Services</button>
                            </div>
                            <div style={{
                                borderRadius: 12,
                                background: '#fff3e5',
                                height: '100%',
                                padding: '20px',
                                margin: '20px',
                                boxShadow: "4px 4px 16px 10px rgba(110,110,110,0.09) "
                            }} className='wrap-text-white'>
                                <div style={{display: 'flex'}}>
                                    <div className='circle' style={{background: 'grey'}}></div>
                                    <div className='circle purplex' style={{width: 60, height: 13}}></div>
                                    <span className="material-symbols-outlined grayx" >
                                        church
                                    </span>
                                </div>
                                <p style={{color: '#555'}}>"Effective emergency response and medical aid services across
                                    Scotland reduce critical delays, providing timely care that saves lives, improves patient outcomes, avoid and prevent disasters,and strengthens overall public health and safety."</p>
                                <button className='shGreen greenx'>Save Scotland</button>
                            </div>
                        </div>
                    </div>
                </div>

            </div>

        </div>);
}