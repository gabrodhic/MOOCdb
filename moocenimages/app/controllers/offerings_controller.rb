class OfferingsController < ApplicationController
  before_filter :authenticate_user!

  def new
    @visualization = Visualization.find(params[:viz_id])

    @offering = Offering.new(:visualization_id => params[:viz_id])
  end

  def create
    @visualization = Visualization.find(params[:viz_id])
    @offering = Offering.create(params[:offering].merge({:visualization_id => @visualization.id,}))
    upload = Upload.create(
        :visualization_id => @visualization.id,
        :content => params[:offering][:content],
        :user_id => current_user.id,
        :visualization_step_id => 5,
        :offering_id => @offering.id
    )

    @offering_id = @offering.id
    redirect_to @visualization
  end
end