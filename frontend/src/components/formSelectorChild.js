import React from 'react';
import Form1 from './form1'
import Form2 from './form2'
import Form3 from './form3'
import Form4 from './form4'
class FSChild extends React.Component{
    render(){
        if(this.props.form1){
            return(
                <div >
                    <h1>Find Target Face and Corrupt</h1>
                    <Form1 />
                </div>
            )
        }else if(this.props.form2){
            return(
                <div >
                    <h1>Find All Faces</h1>
                    <Form2 />
                </div>
            )
        }else if(this.props.form3){
            return(
                <div >
                    <h1>Find Target Face</h1>
                    <Form3 />
                </div>
            )
        }else if(this.props.form4){
            return(
                <div >
                    <h1>My Face Detection</h1>
                    <Form4 />
                </div>
            )
        }else{
            return(
                <div>
                    <h1>Select Form</h1>
                </div>
            )
        }
    }
}
export default FSChild;