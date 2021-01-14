import React from 'react';

class ImageContainer extends React.Component{
    render(){
        if(this.props.isLoad && this.props.image!=null){
            return(
                <div class="imgContainer">
                    <img src={`data:image/jpeg;base64,${this.props.image}`} alt="" ></img>
                </div>
            )
        }else if(this.props.isLoad && this.props.image==null){
            return(
                    <div class="loader">                    
                        <img src="../blocks.gif" alt=""></img>
                    </div>
            )
        }else{
            return(
                <div>
                </div>
            )
        }
    }
}
export default ImageContainer;