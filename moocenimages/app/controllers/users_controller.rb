class UsersController < ApplicationController
  def index
    @users = User.find(:all)
  end

  def new
    @user = User.new
  end

  def create
    @user = User.new(params[:user])
    respond_to do |format|
      if @user.save
        format.html { redirect_to root_path }
        format.json { render json: @user, status: :created, location: @user }
      else
        format.html { render action: "new" }
        format.json { render json: @user.errors, status: :unprocessable_entity }
      end
    end
  end

  def edit
    @user = current_user
  end

  def update
    @user = current_user
    if @user.update_attributes(params[:user])
      flash[:notice] = "You have sucessfully updated your profile."
    end
    redirect_to users_path
  end

  def destroy
    User.find(params[:id]).destroy
    redirect_to :back
  end
end
