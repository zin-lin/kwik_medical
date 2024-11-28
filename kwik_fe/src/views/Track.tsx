import React, {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import axios from "axios";
import { io, Socket } from 'socket.io-client';

interface DATA {
    cid : string ;

}

export default function Track() {
    const socket: Socket = io('http://localhost:8000');
    const {cid} = useParams();
    const [name, setName] = useState("");
    const [status, setStatus] = useState(0);
    const [hos, setHos] = useState("");
    const [update, setUpdate] = useState("");
    const [am, setAm] = useState("");

    useEffect(()=>{
        // Connect to the WebSocket server
        socket.on('connect', () => {
            console.log('Connected to WebSocket server');

            // Send the caseId to track
            socket.emit('track_document', { doc_id: cid });
        });

        let id = cid!.toString();

        axios.get(`/api/get/${cid}`).then((res) => res.data).then(
            (data)=>{
                console.log(data)
                setName(data['pname']);
                setStatus(data['status']);
                setHos(data['hospital']);
                setAm(data['a_num']);
            }
        );

        // Listen for updates on the document
        socket.on('document_update', (data) => {
                console.log(data);
                setName(data['doc']!['pname']);
                setStatus(data['doc']['status']);
                setHos(data['doc']!['hospital']);
                setAm(data['doc']!['a_num']);
                setUpdate(data['doc']!['doc_id']);
                console.log(update);

        });

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
                    <div style={{
                        borderRadius: 12,
                        background: '#fff',
                        height: 320,
                        padding: '20px',
                        margin: '20px',
                        alignContent: 'center',
                        boxShadow: "4px 4px 16px 10px rgba(110,110,110,0.09) "
                    }} className='wrap-text-white shGreen'>
                        <div style={{display: 'flex'}}>
                            <div className='circle' style={{background: 'grey'}}></div>
                            <div className='circle redx' style={{width: 60, height: 13}}></div>
                            <span className="material-symbols-outlined grayx" style={{color: '#ff8989'}}>
                                        task
                                    </span>
                        </div>
                        <p style={{color: '#555'}}>"The report has been picked up by a hospital and is preparing to
                            dispatch ambulances to the location
                            "</p>

                        <div style={{width: '100%', justifyContent: 'center', alignContent: 'center',}}>
                            <div style={{
                                background: status > 0 ? '#55da93' : '#aaa',
                                width: 60,
                                borderRadius: 30,
                                justifyContent: 'center',
                                alignContent: 'center',
                                paddingTop: 0,
                                height: 60,
                                margin: 'auto'
                            }}>
                             <span className="material-symbols-outlined grayx" style={{color: '#fff', fontSize: 33}}>
                                        done_outline
                             </span>
                            </div>
                        </div>
                    </div>

                    <div style={{
                        borderRadius: 12,
                        background: '#fff',
                        height: 320,
                        alignContent: 'center',

                        padding: '20px',
                        margin: '20px',
                        boxShadow: "4px 4px 16px 10px rgba(110,110,110,0.09) "
                    }} className='wrap-text-white shGreen'>
                        <div style={{display: 'flex'}}>
                            <div className='circle' style={{background: 'grey'}}></div>
                            <div className='circle purplex' style={{width: 60, height: 13}}></div>
                            <span className="material-symbols-outlined grayx" style={{color: '#60d6ad'}}>
                                        ambulance
                                    </span>
                        </div>
                        <p style={{color: '#555'}}>"An Ambulance has accepted the request and is currently being
                            dispatched and is heading to incident location
                            "</p>
                        <div style={{width: '100%', justifyContent: 'center', alignContent: 'center',}}>
                            <div style={{
                                background: status > 1 ? '#55da93' : '#aaa',
                                width: 60,
                                borderRadius: 30,
                                justifyContent: 'center',
                                alignContent: 'center',
                                paddingTop: 0,
                                height: 60,
                                margin: 'auto'
                            }}>
                             <span className="material-symbols-outlined grayx" style={{color: '#fff', fontSize: 33}}>
                                        done_outline
                             </span>
                            </div>
                        </div>
                    </div>

                    <div style={{
                        borderRadius: 12,
                        background: '#fff',
                        height: 320,
                        alignContent: 'center',
                        padding: '20px',
                        margin: '20px',
                        boxShadow: "4px 4px 16px 10px rgba(110,110,110,0.09) "
                    }} className='wrap-text-white shGreen'>
                        <div style={{display: 'flex'}}>
                            <div className='circle' style={{background: 'grey'}}></div>
                            <div className='circle bluex' style={{width: 60, height: 13}}></div>
                            <span className="material-symbols-outlined grayx" style={{color: '#e989ff'}}>
                                        done_all
                                    </span>
                        </div>
                        <p style={{color: '#555'}}>"The Ambulance has successfully navigated and has arrived to the
                            incident location and is in the progress of transporting patient.
                            "</p>
                        <div style={{width: '100%', justifyContent: 'center', alignContent: 'center',}}>
                            <div style={{
                                background: status > 2 ? '#55da93' : '#aaa',
                                width: 60,
                                borderRadius: 30,
                                justifyContent: 'center',
                                alignContent: 'center',
                                paddingTop: 0,
                                height: 60,
                                margin: 'auto'
                            }}>
                             <span className="material-symbols-outlined grayx" style={{color: '#fff', fontSize: 33}}>
                                        done_outline
                             </span>
                            </div>
                        </div>
                    </div>

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
                        background: '#fff',
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
                        <p style={{color: '#555'}}>{name}</p>

                    </div>

                    <div style={{
                        borderRadius: 12,
                        background: '#fff',
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
                        <p style={{color: '#555'}}>{hos}
                            </p>

                    </div>

                    <div style={{
                        borderRadius: 12,
                        background: '#fff',
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
                        <p style={{color: '#555'}}>{am}</p>

                    </div>

                </div>
            </div>

        </div>
    );
}