import {createSlice} from "@reduxjs/toolkit";
interface RegisterState {
    value: boolean // initial State
    ,
    text: string // initial State
    ,
    selected : {v1: string, v2: string, v3:string, v4:string } // initial State
    ,
    enucs: string
}

// Define the initial state using that type
const initialState: RegisterState = {
    value: false,
    text: 'Sign in to Store',
    selected: {v1: '#ce6565', v2: '#eee', v3: '#eee', v4: '#eee'},
    enucs: ""
}

/**
 * Reducers
 */
export const authSlice = createSlice({
    extraReducers: undefined, initialState: {value: false, text:'Sign In to Store', selected: {v1: '#ce6565', v2: '#888', v3: '#888', v4: '#888'}, enucs:""},
    name: "auth", reducers: {
        LogOut:(state)=> {
            state.value =false;
        },
        Login: (state)=>{
            state.value = true;
        },
        toLogin:(state)=> {
            state.text = "Sign In to Store";
        },
        toRegister: (state)=>{
            state.text = "Register Now";
        },
        toHome: (state)=>{
            state.selected =  {v1: '#ce6565', v2: '#888', v3: '#888', v4: '#888'}
        },
        toAbout: (state)=>{
            state.selected =  {v1: '#888', v2: '#ce6565', v3: '#888', v4: '#888'}
        },
        toShop: (state)=>{
            state.selected =  {v1: '#888', v2: '#888', v3: '#ce6565', v4: '#888'}
        },
        toProfile: (state)=>{
            state.selected =  {v1: '#888', v2: '#888', v3: '#888', v4: '#ce6565'}
        },
        resetAllVs: (state)=>{
            state.selected =  {v1: '#888', v2: '#888', v3: '#888', v4: '#888'}
        },
        addText: (state, adder )=>{
            state.enucs += adder;
        }
    }
});
export const {Login, LogOut, toLogin, toRegister, toHome, toShop, toAbout, toProfile, resetAllVs} = authSlice.actions;
export default authSlice.reducer;