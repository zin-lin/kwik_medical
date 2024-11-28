import React, {useEffect, useRef, useState} from "react";
import {Link, useNavigate} from "react-router-dom";
import axios from "axios";

export default function Cases () {

    const [cases, setCases] = useState([]);
    const navigate = useNavigate();
    useEffect(()=>{
        axios.get("/api/getAll").then(res=>res.data
        ).then(data=> {
            setCases(data)
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
                            <div style={{
                                borderRadius: 20, margin: '40px', background: '#fff', width: '80%', minHeight: 140,
                                boxShadow: "4px 4px 16px 10px rgba(110,110,110,0.09) ", maxWidth: 1100, padding: 30
                            }} onClick={()=>{
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
                                        <p className='highlight'>#{caseD['hospital']}</p>
                                    </div>
                                    <div style={{marginLeft: 20,}}>
                                        <p className='highlight'>{caseD['a_num'] !== 'N/A'? caseD['a_num']: '#is_open'}</p>
                                    </div>
                                </div>

                                <div style={{
                                    display: 'flex',
                                    alignContent: 'center',
                                    alignItems: 'center',
                                    justifyContent: 'center'
                                }}>
                                     <span className="material-symbols-outlined grayx"
                                           style={{color: '#aaa', fontSize: 33, marginRight: 20, marginLeft: 10}}>
                                            task
                                    </span>

                                    <hr style={{width: '45%' ,  background:caseD['status'] > 1? '#7bffa0':'#fefefe'}}/>

                                    <span className="material-symbols-outlined grayx"
                                          style={{color: '#aaa', fontSize: 33, marginRight: 20}}>
                                            church
                                    </span>
                                    <hr style={{width: '45%', background:caseD['status'] > 2? '#7bffa0':'#fefefe'}}/>

                                    <span className="material-symbols-outlined grayx"
                                          style={{color: '#aaa', fontSize: 33, marginRight: 20}}>
                                            done_all
                                    </span>
                                </div>

                            </div>
                        );
                    })
                }
            </div>
        </div>
    );

}