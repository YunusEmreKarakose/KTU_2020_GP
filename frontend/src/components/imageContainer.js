import React from 'react';

class ImageContainer extends React.Component{
    render(){
        if(this.props.isLoad){
            return(
                <div>
                    <img src={`data:image/jpeg;base64,${this.props.image}`} ></img>
                </div>
            )
        }else{
            return(
                <div>
                    <h1>loading</h1>
                </div>
            )
        }
    }
}
export default ImageContainer;