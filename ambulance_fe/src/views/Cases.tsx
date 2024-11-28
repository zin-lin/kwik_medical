import React, {useEffect, useRef, useState} from "react";
import {Link, useNavigate} from "react-router-dom";
import axios from "axios";

export default function Cases () {

    const [cases, setCases] = useState([]);
    const navigate = useNavigate();
    useEffect(()=>{
        axios.get('/api/authed').then(res=>res.data).then(data=> {
            if (data['id'] === '')
                navigate('/');
        })


        axios.get("/api/getAll").then(res=>res.data
        ).then(data=> {
            setCases(data)
            console.log(data)
        })
    }, [])

    return (
        <div className='page'>
            <link rel="stylesheet"
                  href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"/>
            <div style={{margin:0, marginBottom:0, justifyContent:'center', width:'100%', justifyItems:'center',
                display:'flex', flexDirection:'column', alignItems:'center'

                
            }}>
                {
                    cases.map((caseD, index) =>{
                        return (
                            caseD['status'] <2 ? <div style={{
                                borderRadius: 20, margin: '40px', background: 'rgba(31,43,50,0.39)', width: '80%', minHeight: 140,
                                maxWidth: 1100, padding: 30
                            }} onClick={()=>{
                                axios.get(`/api/update/${caseD['id']}`).then(res=>console.log(res.data)).catch(e => console.log(e))
                                navigate(`/track/${caseD['id']}`);
                            }}>
                                <div style={{display: 'flex', alignContent: 'center', alignItems: 'center'}}>
                                    <div style={{marginRight: 20,}}>

                                    </div>
                                    <span className="material-symbols-outlined grayx"
                                          style={{color: '#aaa', fontSize: 33, marginRight: 20}}>
                                            person
                                    </span>
                                    <div
                                        style={{display: 'flex'}}> {(caseD!['pname']) !== null ? caseD!['pname'] : 'John/Jane Doe'}
                                    </div>
                                    <div style={{marginLeft: 20,}}>
                                        <p className='orangex shOrange' style={{padding:10, borderRadius:7}}>#{caseD['hospital']}</p>
                                    </div>
                                    <div style={{marginLeft: 20,}}>
                                        <p className='orangex shOrange' style={{padding:10, borderRadius:7}}>{caseD['a_num'] !== 'N/A'? caseD['a_num']: '#is_open'}</p>
                                    </div>
                                </div>

                                <div style={{
                                    display: 'flex',
                                    alignContent: 'center',
                                    alignItems: 'center',
                                    justifyContent: 'center'
                                }}>
                                     <span className="material-symbols-outlined grayx"
                                           style={{color: '#78b84e', fontSize: 33, marginRight: 20, marginLeft: 10}}>
                                            task
                                    </span>

                                    <hr style={{width: '45%' ,  background:caseD['status'] > 1? '#7bffa0':'#444'}}/>

                                    <span className="material-symbols-outlined grayx"
                                          style={{color: '#4fcdd1', fontSize: 33, marginRight: 20, marginLeft:20}}>
                                            church
                                    </span>
                                    <hr style={{width: '45%', background:caseD['status'] > 2? '#7bffa0':'#444'}}/>

                                    <span className="material-symbols-outlined grayx"
                                          style={{color: '#dc7070', fontSize: 33, marginLeft: 20}}>
                                            done_all
                                    </span>
                                </div>
                                <div style={{padding:30}}>
                                    <button className='redx shRed'> Take Case</button>
                                </div>
                            </div> : <div></div>
                        );
                    })
                }
            </div>
        </div>
    );

}