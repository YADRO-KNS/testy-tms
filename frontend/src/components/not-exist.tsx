import React from 'react';
import Container from "@mui/material/Container";

const NotExist: React.FC = () => {
    return (
        <Container component="main" maxWidth="xs">
            <div style={{
                fontSize: 18.5,
                alignItems: 'center',
                flexDirection: 'column',
                display: 'flex',
            }}>
                <div style={{fontSize: 170}}>
                    404
                </div>
                Данной страницы не существует
            </div>
        </Container>
    );
}

export default NotExist