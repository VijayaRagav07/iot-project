import streamlit as st
import qrcode
from io import BytesIO
import base64
from PIL import Image

# Set page config
st.set_page_config(
    page_title="QR Code Generator",
    page_icon="📱",
    layout="centered"
)

def generate_qr_code(url):
    """Generate QR code for given URL"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes for display
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)
    
    return buffer

def get_app_url():
    """Get the current app URL"""
    # Replace this with your actual deployed URL after deployment
    deployed_url = "https://your-app-name.streamlit.app"  # Update this!
    
    # Check if running locally
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8501))
        sock.close()
        if result == 0:
            return "http://localhost:8501"  # Running locally
    except:
        pass
    
    # Return deployed URL
    return deployed_url

def main():
    # Header
    st.title("📱 QR Code Website Generator")
    st.markdown("---")
    
    # Get current app URL
    app_url = get_app_url()
    
    # Display current URL
    st.subheader("🌐 Current Website URL:")
    st.code(app_url)
    
    # Generate QR code
    st.subheader("📷 QR Code for this Website:")
    
    try:
        qr_buffer = generate_qr_code(app_url)
        
        # Display QR code
        st.image(qr_buffer, caption="Scan this QR code to access the website", width=300)
        
        # Download button
        st.download_button(
            label="📥 Download QR Code",
            data=qr_buffer.getvalue(),
            file_name="website_qr_code.png",
            mime="image/png"
        )
        
    except Exception as e:
        st.error(f"Error generating QR code: {e}")
    
    # Instructions
    st.markdown("---")
    st.subheader("📋 How to Use:")
    st.markdown("""
    1. **Deploy this app** to Streamlit Cloud or your preferred hosting platform
    2. **Update the URL** in the code with your actual deployed URL
    3. **Share the QR code** - anyone can scan it to access your website
    4. **Download the QR code** using the button above for printing or sharing
    """)
    
    # Custom URL section
    st.markdown("---")
    st.subheader("🔗 Generate QR for Custom URL:")
    
    custom_url = st.text_input("Enter any URL:", placeholder="https://example.com")
    
    if custom_url:
        if custom_url.startswith(('http://', 'https://')):
            try:
                custom_qr_buffer = generate_qr_code(custom_url)
                st.image(custom_qr_buffer, caption=f"QR Code for: {custom_url}", width=300)
                
                st.download_button(
                    label="📥 Download Custom QR Code",
                    data=custom_qr_buffer.getvalue(),
                    file_name="custom_qr_code.png",
                    mime="image/png",
                    key="custom_download"
                )
            except Exception as e:
                st.error(f"Error generating custom QR code: {e}")
        else:
            st.warning("Please enter a valid URL starting with http:// or https://")
    
    # Footer
    st.markdown("---")
    st.markdown("**Built with Streamlit and Python** 🐍")

if __name__ == "__main__":
    main()