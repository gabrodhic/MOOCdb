class SessionsController < ApplicationController

  def new
  end

  def create
    if signed_in?
      flash[:error] = "Please sign out before signing into a different account."
      redirect_to current_user
      return
    end
    user = User.find_by(email: params[:session][:email].downcase)
    if user && user.authenticate(params[:session][:password])
      sign_in user
      redirect_back_or user
    else
      flash.now[:error] = 'Invalid email/password combination' #Almost!
      render 'new'
    end
  end
 
  def destroy
    sign_out
    redirect_to root_url
  end
end
