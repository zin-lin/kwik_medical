import React from "react";

export default function Login() {
    return (
        <div className='page' >
            <link rel="stylesheet"
                  href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"/>
            <div style={{
                width: '100%',
                height: '100%',
                display: 'flex',
                flex: 1,
                marginTop: 0 ,
                position: 'relative',
                transition: '0.6s ease',
                opacity: 1,
                justifyContent: 'center',
                alignItems: 'center'
            }} >

                <div style={{display: "flex", justifyContent: "center", height: '100%', alignItems: 'center'}}>
                    <div style={{
                        background: 'rgb(250,250,250,1.0    )',
                        height: '80%',
                        width: '80%',
                        maxHeight: 380,
                        maxWidth: 500,
                        minWidth: 300,
                        minHeight: 350,
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
                            }}>
                                <div style={{display: 'flex', alignItems: 'center', marginLeft: 26}}>
                                    <span style={{color: '#aaa', fontSize: 19, marginRight: 10}}
                                          className="material-symbols-outlined">
                                         license
                                    </span><p style={{color: '#aaa', fontSize: 14}}>Plate Number</p>
                                </div>
                                <input placeholder='@plate number' className='noner' id="email"/>
                                <br/>
                                <div style={{display: 'flex', alignItems: 'center', marginLeft: 26}}>
                                        <span style={{color: '#aaa', fontSize: 19, marginRight: 10}}
                                              className="material-symbols-outlined">
                                             emergency
                                        </span> <p style={{color: '#aaa', fontSize: 14}}>Hospital Code</p>
                                </div>
                                <input placeholder='code' className='noner' type='password' id="password"/>
                                <button className='redx shRed' type="submit" style={{
                                    margin: 20,
                                    width: 170,
                                    paddingTop: 8,
                                    paddingBottom: 8
                                }}>Login As Ambulance
                                </button>
                            </form>
                        </div>
                    </div>

                </div>
            </div>
        </div>

    );
}