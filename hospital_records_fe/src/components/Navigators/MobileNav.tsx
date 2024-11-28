import React from "react";
import {Link, useNavigate} from "react-router-dom";
import {useAuthDispatch, useAuthSelector} from "../../redux/hook";
import {toHome, toAbout, toShop, toProfile} from "../../redux/authState";

const navSty = {
    fontSize:16, margin:10
}

const napierColor = {
    color:"#FF5757"
}

export default function MobileNav () {
    const selected = useAuthSelector(state => state.auth.selected);
    const dispatch = useAuthDispatch();
    const navigate = useNavigate();
    return (
        <div className='mobile-nav'>
            <div style={{display: 'flex', marginTop: '15px'}}>
                <div className='mobile-nav-item4' >
                    <Link to='/' onClick={()=>dispatch(toHome())}>
                    <span className="material-symbols-outlined" style={{color: selected.v1}}>
                        home
                    </span>
                    </Link>
                </div>

                <div className='mobile-nav-item4' >
                    <Link to='/about' onClick={()=>dispatch(toAbout())}>
                    <span className="material-symbols-outlined" style={{color: selected.v2}}>
                    info
                    </span>
                    </Link>
                </div>


            </div>
        </div>
    );
}